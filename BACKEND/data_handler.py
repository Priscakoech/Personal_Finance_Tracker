
import requests
import time
from BACKEND.custom_markdown_formatter import MarkdownFormatter

OPENAI_API_KEY = "YOUR-OPEN-API-KEY"

class DataHandler:
    def __init__(self):
        self.parser = None
        self.all_transactions = []
        self.wallets = {}
        self.last_api_call_time = 0

    def generate_insight(self, category, data, user_name):
        insight_context = (
            f"You are a smart assistant for this Personal Finance Tracker app used by {user_name}. "
            "Your job is to analyze personal financial trends from user data and generate brief, insightful summaries. "
            "The data is a simple dictionary identified by a period (Daily, Weekly, Monthly, Yearly, or General)."
            "You can easily identify the data's period by simply looking at the Graph Data for either Expenditure or Income."
            "Daily has a list length of 24, meaning 24 hours. The first value represents 12AM, all the way upto the last value which is 11PM."
            "Weekly has 7, meaning 7 days. The first value is Monday, all the way upto Sunday."
            "Monthly has varying values ranging between 28 to 31 representing the number of days for the current month."
            "Yearly has just 12, representing the 12 months of the year."
            "For General, it doesn't have Graph Data, rather, it has just Expenditure and Income Categories, accompanied by their values."
            "The goal is to give short but helpful financial insight in under 63 words. "
            "Only use these markdown styles: #title, **subtitle**, *italics*, -lists. "
            "Currency is in Kenyan Shillings (Ksh)."
            "Using this, you can easily know when is today, what week it is, and what month it is..."
            "Use plain language. If no income or expenses exist for a period, mention that. "
            "Include only relevant categories that had values greater than 0."
            "DO NOT mention dates/week number/month or year in your responses."
            "Hint out some very insightful comments... you can also advice me on how I should likely manage my funds."
        )

        current_time = time.time()
        if current_time - self.last_api_call_time < 15:
            return MarkdownFormatter().format_text(text="Too many requests. Please wait before requesting again.")

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": insight_context},
                {"role": "user", "content": f"generate a {category} insight based on this data {data}"}
            ],
            "temperature": 0.7
        }

        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
            response.raise_for_status()
            result = response.json()
            message = result["choices"][0]["message"]["content"]
            self.last_api_call_time = current_time
            return MarkdownFormatter().format_text(text=message)
        except Exception:
            return MarkdownFormatter().format_text(text="Could not generate insight...try again later.")

    def transactions(self):
        mpesa = [tx for tx in self.all_transactions if "mpesa" in tx["acc_type"]]
        crypto = [tx for tx in self.all_transactions if "crypto" in tx["acc_type"]]

        return {
            "all": self.all_transactions,
            "mpesa": mpesa,
            "crypto": crypto
        }
