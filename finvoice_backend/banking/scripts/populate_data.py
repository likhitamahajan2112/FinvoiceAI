import random
from banking.models import User, Transaction

def run():
    # Clear old data
    User.objects.all().delete()
    Transaction.objects.all().delete()

    # Generate 50 users
    for i in range(1, 51):
        account_number = f"ACC{i:05d}"
        pin = f"{random.randint(1000, 9999)}"
        balance = random.randint(1000, 100000)

        # Create user directly (no duplicates)
        user = User.objects.create(
            account_number=account_number,
            pin=pin,
            balance=balance,
            username=account_number  # required by AbstractUser
        )

        # Generate 10 transactions per user
        for _ in range(10):
            amount = random.randint(100, 5000)
            tx_type = random.choice(['credit', 'debit'])
            description = random.choice([
                "ATM Withdrawal", "Salary Credit", "Online Purchase",
                "Bill Payment", "Fund Transfer", "Cash Deposit"
            ])
            Transaction.objects.create(
                user=user,
                amount=amount,
                type=tx_type,
                description=description
            )

    print("✅ Successfully populated 50 users with transactions!")