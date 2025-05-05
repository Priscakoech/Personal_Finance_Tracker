
import os
import threading
import regex as re
import requests
import csv
from calendar import monthrange
from datetime import datetime
from collections import defaultdict
from datetime import datetime
from kivy.utils import platform


class MpesaMessageParser:
    def __init__(self, raw_data: list, user_name=None, user_data_store=None, firebase=None, id_token=None, uid=None, knowledge_base=None):
        self.firebase = firebase
        self.id_token = id_token
        self.u_id = uid
        self.knowledge_base = knowledge_base or {}

        self.year = datetime.now().year
        self.current_year_formatted = f"/{str(self.year)[2:]}"
        self.current_month_num_of_days = monthrange(datetime.today().year, datetime.today().month)[1]

        self.yearly_transactions = defaultdict(list)
        self.monthly_transactions = defaultdict(list)
        self.weekly_transactions = defaultdict(list)
        self.daily_transactions = defaultdict(list)
        self.formatted_transactions = []

        self.all_messages = raw_data
        self.user_name, self.user_phone = user_name, ""
        self.user_data_store = user_data_store
        self.daily_expenses = 0
        self.daily_income = 0
        self.expense_categories = {cat: 0 for cat in ["Friends & Family", "Housing", "Utilities", "Groceries", "Miscellaneous"]}
        self.income_categories = {cat: 0 for cat in ["Friends & Family", "Salary", "Investments", "Side Gigs", "Other Income"]}
        self.hourly = [0]*24
        self.weekly = [0]*7
        self.monthly = [0]*monthrange(self.year, datetime.now().month)[1]
        self.yearly = [0]*12
        self.csv_data = []

    def date_extractor(self, msg):
        match = re.search(r'on (\d{1,2}/\d{1,2}/\d{2}) at (\d{1,2}:\d{2} [APM]{2})', msg)
        if not match:
            match = re.search(r'On (\d{1,2}/\d{1,2}/\d{2}) at (\d{1,2}:\d{2} [APM]{2})', msg)

        if match:
            date_str = match.group(1)
            time_str = match.group(2)
            full_str = f"{date_str} {time_str}"
            return datetime.strptime(full_str, "%d/%m/%y %I:%M %p")
        return None

    def format_transaction(self, msg):
        self.user_phone = self.user_data_store.get("user_phone")["user_phone"] if self.user_data_store.exists("user_phone") else ""
        user_acc = f"{self.user_phone}\n{self.user_name}"
        tx_data = {
            "sr_name": "Unknown",
            "amount": "Ksh 0.00",
            "t_time": "Unknown",
            "acc_type": "assets/images/mpesa_icon.png",
            "t_id": "N/A",
            "t_fee": "Ksh. 0.00",
            "sender_acc": "N/A",
            "receiver_acc": "N/A",
            "t_category": "Uncategorized"
        }

        lower_msg = msg.lower()

        # Transaction ID
        tx_id_match = re.search(r'MPESA:\s*\n*(\w+)', msg)
        if "congratulations" in lower_msg: tx_id_match = re.search(r'MPESA:\s*\n*Congratulations! (\w+)', msg)
        if tx_id_match: tx_data["t_id"] = tx_id_match.group(1).strip()

        # Amount
        amount_match = re.search(r'Ksh[ ]*([\d,]+\.\d{2})', msg)
        if amount_match:
            amount = amount_match.group(1).strip()
            tx_data["amount"] = f"+ {amount}" if "received" in msg.lower() or "reversed successfully" in msg.lower() else f"- {amount}"

        # Time
        tx_date = self.date_extractor(msg)
        if tx_date: tx_data["t_time"] = tx_date.strftime("%B %d, %Y, at %I:%M %p")

        # Transaction Fee
        fee_match = re.search(r'Transaction cost[,]?\s*Ksh[.\s]*([\d,]+\.\d{2})', msg)
        if fee_match: tx_data["t_fee"] = f"Ksh. {fee_match.group(1)}"

        # === Transaction Case Handlers === #
        # Case: Received incentive/payment
        if "incentive" in lower_msg or "reward" in lower_msg:
            name_match = re.search(r'from\s+(.*?)\s+on', msg)
            if name_match:
                name = name_match.group(1).strip()
                tx_data["sr_name"] = name
                tx_data["sender_acc"] = f"{name}"
                tx_data["receiver_acc"] = user_acc
                tx_data["t_category"] = "Other Income"
                self.override_with_kb(tx_data=tx_data)

        # Case: M-Shwari transfers
        elif "m-shwari" in lower_msg:
            if "to m-shwari" in lower_msg:
                tx_data["t_category"] = "Savings"
                self.override_with_kb(tx_data=tx_data)
                tx_data["receiver_acc"] = "M-Shwari\nAccount"
                tx_data["sender_acc"] = user_acc
                tx_data["sr_name"] = "M-Shwari"
            elif "from m-shwari" in lower_msg:
                tx_data["t_category"] = "Savings Withdrawal"
                self.override_with_kb(tx_data=tx_data)
                tx_data["sender_acc"] = "M-Shwari\nAccount"
                tx_data["receiver_acc"] = user_acc
                tx_data["sr_name"] = "M-Shwari"

        # Case: Fuliza repayment
        elif "fuliza" in lower_msg and "pay" in lower_msg:
            tx_data["t_category"] = "Loan Repayment"
            self.override_with_kb(tx_data=tx_data)
            tx_data["sr_name"] = "Fuliza M-PESA"
            tx_data["sender_acc"] = user_acc
            tx_data["receiver_acc"] = "Fuliza\nSafaricom"

        # Case: Airtime purchase
        elif "airtime" in lower_msg or "bought ksh" in lower_msg:
            tx_data["sr_name"] = "Safaricom"
            tx_data["sender_acc"] = user_acc
            tx_data["receiver_acc"] = "Safaricom\nAirtime"
            tx_data["t_category"] = "Miscellaneous"
            self.override_with_kb(tx_data=tx_data)

        # Case: Till or Paybill payment (paid to)
        elif "paid to" in lower_msg:
            paid_to_match = re.search(r'paid to\s+([^.]+)', msg)
            if paid_to_match:
                name = paid_to_match.group(1).strip()
                tx_data["sr_name"] = name
                tx_data["receiver_acc"] = f"{name}"
                tx_data["sender_acc"] = user_acc
                tx_data["t_category"] = "Groceries"
                self.override_with_kb(tx_data=tx_data)

        # Case: Sent to
        elif "sent to" in lower_msg:
            sr_match = re.search(r'sent to\s+(.+?)\s+(\d{10})', msg)
            t_category = "Friends & Family"

            if not sr_match: sr_match = re.search(r'sent to\s+(.+?)\s+on', msg)
            if "for account" in lower_msg:
                sr_match = re.search(r'sent to\s+(.+?)\s+for account\s+(.+? | \d.+?)', msg)
                t_category = "Miscellaneous"

            if sr_match:
                name = sr_match.group(1).strip()
                try: phone = sr_match.group(2)
                except Exception: phone = ""
                tx_data["sr_name"] = name
                if "for account" in lower_msg: tx_data["receiver_acc"] = f"{phone}"
                else: tx_data["receiver_acc"] = f"{phone}\n{name}"
                tx_data["sender_acc"] = user_acc
                tx_data["t_category"] = t_category
                self.override_with_kb(tx_data=tx_data)

        # Case: Received from
        elif "received" in lower_msg:
            sr_match = re.search(r'from\s+(.+?)\s+(\d{9,10})', msg)
            if not sr_match: sr_match = re.search(r'from\s+(.+?)\s+on', msg)
            if sr_match:
                name = sr_match.group(1).strip()
                try: phone = sr_match.group(2)
                except Exception: phone = ""
                tx_data["sr_name"] = name
                tx_data["sender_acc"] = f"{phone}\n{name}"
                tx_data["receiver_acc"] = user_acc

                if len(tx_data["amount"]) > 10: tx_data["t_category"] = "Other Income"
                else: tx_data["t_category"] = "Friends & Family"
                self.override_with_kb(tx_data=tx_data)

        # Case: Withdrawals
        elif "withdraw" in lower_msg:
            tx_data["t_category"] = "Cash Withdrawal"
            self.override_with_kb(tx_data=tx_data)
            tx_data["sender_acc"] = "M-PESA\nAgent"
            tx_data["receiver_acc"] = user_acc
            name_match = re.search(r'from\s+(.*?)\s+(?:New|Transaction)', msg)
            if name_match: tx_data["sr_name"] = name_match.group(1).strip()

        # Case: Give
        elif "give" in lower_msg:
            sr_match = re.search(r'cash to\s+(.+?)\s+New', msg)
            if sr_match:
                name = sr_match.group(1).strip()
                tx_data["sr_name"] = name
                tx_data["sender_acc"] = user_acc
                tx_data["receiver_acc"] = f"{name}"
                tx_data["t_category"] = "Miscellaneous"
                self.override_with_kb(tx_data=tx_data)

        # Case: KCB M-PESA & Lock Savings
        elif "transfered to kcb m-pesa" in lower_msg:
            tx_data["sr_name"] = "KCB M-PESA"
            tx_data["sender_acc"] = user_acc
            tx_data["receiver_acc"] = "KCB M-PESA"
            tx_data["t_category"] = "Savings"
            self.override_with_kb(tx_data=tx_data)

        elif "from your kcb m-pesa account" in lower_msg:
            tx_data["sr_name"] = "KCB M-PESA"
            tx_data["sender_acc"] = "KCB M-PESA"
            tx_data["receiver_acc"] = user_acc
            tx_data["t_category"] = "Savings Withdrawal"
            self.override_with_kb(tx_data=tx_data)

        elif "transfered to lock savings account" in lower_msg:
            tx_data["sr_name"] = "Lock Savings Account"
            tx_data["sender_acc"] = user_acc
            tx_data["receiver_acc"] = "Lock Savings Account"
            tx_data["t_category"] = "Savings"
            self.override_with_kb(tx_data=tx_data)

        # Case: M-PESA Reversals
        elif "reversed successfully" in lower_msg:
            tx_data["sr_name"] = "M-PESA Reversal"
            tx_data["sender_acc"] = re.search(r'in favour of\s+(.+?)\s+has', msg).group(1).strip()
            tx_data["receiver_acc"] = user_acc
            tx_data["t_category"] = "Other Income"
            self.override_with_kb(tx_data=tx_data)

        return tx_data

    def override_with_kb(self, tx_data):
        sr_name = tx_data.get("sr_name")
        if self.knowledge_base and sr_name in self.knowledge_base:
            tx_data["t_category"] = self.knowledge_base[sr_name]

    def repopulate_firebase(self):
        if not self.formatted_transactions:
            print("No transactions to back up.")
            return

        for tx in self.formatted_transactions: self.override_with_kb(tx)
        mpesa_balance = self.get_mpesa_balance()
        general_insight_vals = self.get_general_insight_values()
        piechart_data = self.get_pie_chart_data()
        all_insights = self.get_insights()

        backup_data = {
            "MPESA Balance": mpesa_balance,
            "General Insight": general_insight_vals,
            "All Insights": all_insights,
            "Piechart Data": piechart_data,
            "Formatted Transactions": self.formatted_transactions
        }

        threading.Thread(
            target=self.save_parsed_data_to_firebase,
            args=(backup_data,)
        ).start()

    def get_parsed_msgs(self):
        all_msgs = self.all_messages

        for msg in all_msgs:
            if "confirmed" in msg.lower() and self.current_year_formatted in msg and "your account balance was" not in msg.lower() and "Fuliza M-PESA amount is" not in msg:
                self.yearly_transactions[str(self.year)].append(msg)

        for msg in self.yearly_transactions[str(self.year)]:
            tx_date = self.date_extractor(msg)
            if tx_date:
                month_key = tx_date.strftime("%B %Y")
                self.monthly_transactions[month_key].append(msg)

                week_key = f"Week {tx_date.isocalendar().week} of {tx_date.year}"
                self.weekly_transactions[week_key].append(msg)

                day_key = tx_date.strftime("%B %d, %Y")
                self.daily_transactions[day_key].append(msg)

            tx_formatted = self.format_transaction(msg)
            self.formatted_transactions.append(tx_formatted)

        self.repopulate_firebase()

        return self.formatted_transactions

    def get_mpesa_balance(self):
        recent_transaction = self.yearly_transactions[str(self.year)][0]  
        bal_match = re.search(r'New M-PESA balance is Ksh[ ]*([\d,]+\.\d{2})', recent_transaction)

        if bal_match:
            bal_as_str = bal_match.group(1).strip()
            bal_as_float = float(bal_as_str.replace(",", ""))
            return bal_as_float

    def get_knowledge_base(self):
        tx_knowledge_base = {}
        for tx in self.formatted_transactions:
            kb_key = tx["sr_name"]
            kb_value = tx["t_category"]
            tx_knowledge_base[kb_key] = kb_value

        return tx_knowledge_base

    def get_general_insight_values(self):
        income_totals = {}
        expense_totals = {}

        for tx in self.formatted_transactions:
            try:
                category = tx["t_category"]
                raw_amount = tx["amount"].strip()
                value = int(float(raw_amount[2:].replace(",", "")))

                if raw_amount.startswith("+"):
                    income_totals[category] = income_totals.get(category, 0) + value
                else:
                    expense_totals[category] = expense_totals.get(category, 0) + value

            except Exception as e:
                print(f"Error parsing category total for {tx['t_id']}: {str(e)}")

        return {
            "Income": income_totals,
            "Expense": expense_totals
        }

    def get_insights(self):
        def initialize_categories(category_type):
            if category_type == "income":
                return {
                    "Friends & Family": 0,
                    "Salary": 0,
                    "Investments": 0,
                    "Side Gigs": 0,
                    "Other Income": 0
                }
            else:
                return {
                    "Friends & Family": 0,
                    "Housing": 0,
                    "Utilities": 0,
                    "Groceries": 0,
                    "Miscellaneous": 0
                }

        def summarize(period_check_fn, graph_type="yearly"):
            now = datetime.now()
            if graph_type == "daily":
                graph_size = 24
                index_fn = lambda dt: dt.hour
            elif graph_type == "weekly":
                graph_size = 7
                index_fn = lambda dt: dt.weekday()
            elif graph_type == "monthly":
                graph_size = monthrange(now.year, now.month)[1]
                index_fn = lambda dt: dt.day - 1
            else:
                graph_size = 12
                index_fn = lambda dt: dt.month - 1

            income_categories = initialize_categories("income")
            expense_categories = initialize_categories("expense")
            income_graph = [0] * graph_size
            expense_graph = [0] * graph_size

            for tx in self.formatted_transactions:
                try:
                    dt = datetime.strptime(tx["t_time"], "%B %d, %Y, at %I:%M %p")
                    if not period_check_fn(dt):
                        continue

                    category = tx["t_category"]
                    raw_amount = tx["amount"].strip()
                    amount = int(float(raw_amount[2:].replace(",", "")))
                    index = index_fn(dt)

                    if raw_amount.startswith("+"):
                        income_categories[category] = income_categories.get(category, 0) + amount
                        income_graph[index] += amount
                    else:
                        expense_categories[category] = expense_categories.get(category, 0) + amount
                        expense_graph[index] += amount

                except Exception as e:
                    print(f"Insight parsing error: {e}")

            return {
                "Total Income": sum(income_categories.values()),
                "Total Expenditure": sum(expense_categories.values()),
                "Income Category": income_categories,
                "Expense Category": expense_categories,
                "Graph Data": {
                    "Income": income_graph,
                    "Expenditure": expense_graph
                }
            }

        now = datetime.now()
        return {
            "Yearly": summarize(lambda dt: dt.year == now.year, graph_type="yearly"),
            "Monthly": summarize(lambda dt: dt.month == now.month and dt.year == now.year, graph_type="monthly"),
            "Weekly": summarize(lambda dt: dt.isocalendar()[1] == now.isocalendar()[1] and dt.year == now.year, graph_type="weekly"),
            "Daily": summarize(lambda dt: dt.date() == now.date(), graph_type="daily")
        }

    def get_pie_chart_data(self):
        income_categories = {
            "Friends & Family": 0,
            "Salary": 0,
            "Investments": 0,
            "Side Gigs": 0,
            "Other Income": 0
        }

        expense_categories = {
            "Friends & Family": 0,
            "Housing": 0,
            "Utilities": 0,
            "Groceries": 0,
            "Miscellaneous": 0
        }

        for tx in self.formatted_transactions:
            amount = float(tx["amount"].replace("+", "").replace("-", "").replace(",", "").strip())
            category = tx["t_category"]

            if "+" in tx["amount"]:
                if category in income_categories:
                    income_categories[category] += amount
            else:
                if category in expense_categories:
                    expense_categories[category] += amount

        def to_percentages(cat_dict):
            total = sum(cat_dict.values())
            if total == 0:
                return {" ": 100, "  ": 0, "   ": 0, "    ": 0, "     ": 0}
            keys = list(cat_dict.keys())
            return {
                k: round((cat_dict[k] / total) * 100)
                for k in keys
            }

        return {
            "Spending": to_percentages(expense_categories),
            "Income": to_percentages(income_categories)
        }

    def save_parsed_data_to_firebase(self, formatted_data):
        if not all([self.firebase, self.id_token, self.u_id]):
            print("Missing Firebase credentials")
            return

        if self.firebase and self.id_token and self.u_id:
            try:
                self.firebase.put_data(
                    id_token=self.id_token,
                    path=f"users/{self.u_id}/parsed_data/mpesa_account",
                    data=formatted_data
                )

                self.knowledge_base = self.sync_knowledge_base(formatted_data["Formatted Transactions"])

            except Exception as e:
                print("Error saving to Firebase:", str(e))

    def sync_knowledge_base(self, formatted_transactions):
        if not all([self.firebase, self.id_token, self.u_id]):
            print("Missing Firebase credentials")
            return {}

        path = f"users/{self.u_id}/knowledge_base"
        existing_kb = self.firebase.get_data(id_token=self.id_token, path=path)

        if not existing_kb or "Knowledge Base" not in existing_kb:
            knowledge_base = self.get_knowledge_base()
            self.firebase.put_data(id_token=self.id_token, path=path, data={"Knowledge Base": knowledge_base})
            print("Knowledge Base created for the first time.")
            return knowledge_base

        else:
            kb = existing_kb["Knowledge Base"]
            updated = False
            for tx in formatted_transactions:
                sr_name = tx["sr_name"]
                category = tx["t_category"]
                if sr_name not in kb:
                    kb[sr_name] = category
                    updated = True
            if updated:
                self.firebase.put_data(id_token=self.id_token, path=path, data={"Knowledge Base": kb})
                print("Knowledge Base updated with new entries.")
            return kb

    def get_mpesa_wallet_details(self):
        self.user_phone = self.user_data_store.get("user_phone")["user_phone"] if self.user_data_store.exists("user_phone") else ""
        kes_wallet_balance = self.get_mpesa_balance()
        usd_wallet_balance = 0
        rate = self.get_kes_to_usd_rate()
        if rate: usd_wallet_balance = f"{(kes_wallet_balance * rate):,.2f}"
        else: usd_wallet_balance = 0

        wallet_details = {
            "mpesa": {
                "icon_path": "assets/images/mpesa_icon.png",
                "left_text": f"M-PESA\n[color=a6a6a6][b][size=13dp]{self.user_phone}[/size][/b]",
                "right_text": f"[size=14dp]Ksh. {kes_wallet_balance:,.2f}\n[color=a6a6a6]≈ $ {usd_wallet_balance}[/size]"
            }
        }

        return {
            "wallet_details": wallet_details,
            "kes_bal": kes_wallet_balance,
            "usd_bal": usd_wallet_balance
        }

    # custom kes-to-usd currency converter
    def get_kes_to_usd_rate(self):
        url = "https://open.er-api.com/v6/latest/KES"
        try:
            response = requests.get(url)
            data = response.json()
            if data["result"] == "success": return data["rates"]["USD"]
            else: return None
        except Exception: return None

    # csv file exporter
    def export_to_csv(self, csv_type="yearly"):
        def filter_transactions_by_type(tx_list, csv_type):
            now = datetime.now()
            filtered = []

            for tx in tx_list:
                try:
                    dt = datetime.strptime(tx.get("t_time", ""), "%B %d, %Y, at %I:%M %p")
                    if csv_type == "daily" and dt.date() == now.date():
                        filtered.append(tx)
                    elif csv_type == "weekly" and dt.isocalendar().week == now.isocalendar().week and dt.year == now.year:
                        filtered.append(tx)
                    elif csv_type == "monthly" and dt.month == now.month and dt.year == now.year:
                        filtered.append(tx)
                    elif csv_type == "yearly":
                        filtered.append(tx)
                except Exception:
                    continue

            return filtered

        tx_data = filter_transactions_by_type(self.formatted_transactions, csv_type)
        filename = f"pft_{csv_type}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        if platform == "android":
            from android.storage import primary_external_storage_path
            export_dir = os.path.join(primary_external_storage_path(), "Download")
        else:
            export_dir = os.path.expanduser("~/Downloads")

        os.makedirs(export_dir, exist_ok=True)
        filepath = os.path.join(export_dir, filename)

        try:
            with open(filepath, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Time", "Sender", "Receiver", "Category", "Amount", "Transaction Fee", "Transaction ID"])

                if not tx_data: writer.writerow(["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"])
                else:
                    for tx in tx_data:
                        dt_str = tx.get("t_time", "")
                        try:
                            date_part, time_part = dt_str.split(", at ")
                        except ValueError:
                            date_part, time_part = dt_str, ""
                        writer.writerow([
                            date_part.strip(),
                            time_part.strip(),
                            tx.get("sender_acc", "").replace("\n", " | "),
                            f"\t{tx.get('receiver_acc', '')}",
                            tx.get("t_category", ""),
                            tx.get("amount", "").split()[1],
                            tx.get("t_fee", "").split()[1],
                            tx.get("t_id", "")
                        ])

            return filepath

        except Exception: return None
