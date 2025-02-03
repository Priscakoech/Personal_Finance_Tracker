# This script is responsible for parsing all transactions, and returning the formatted version of it...

# some starting code...
def transaction_data():
    all_transactions = {
        "M-PESA": {
            "transaction_1": {
                "date": "03/02/25 at 3:14 PM",  # mm/dd/yy
                "activity": "sent",
                "amount": "1100.00",
                "transaction_cost": "0.00",
                "to_acc": "Prisca Koech 0700245601",
                "from_acc": "",
                "balance": "1362.63"
            },

            "transaction_2": {
                "date": "04/02/25 at 4:07 PM",  # mm/dd/yy
                "activity": "received",
                "amount": "1100.00",
                "transaction_cost": "",
                "to_acc": "",
                "from_acc": "Prisca Koech 0700245601",
                "balance": "2462.63"
            }

        },

        "Card": {},
        "PayPal": {},
        "Crypto": {}
    }

    return all_transactions
