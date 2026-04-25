def get_balance(account_number):
    return "₹45,000"

def get_transactions(account_number):
    return [
        {"type": "credit", "amount": 5000, "description": "Salary"},
        {"type": "debit", "amount": 1200, "description": "Groceries"},
        {"type": "debit", "amount": 2500, "description": "Shopping"},
    ]

def transfer_money(sender, receiver, amount):
    return f"Transaction successful. ₹{amount} transferred from account {sender} to account {receiver}"