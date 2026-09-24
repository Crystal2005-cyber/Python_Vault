import json
import os
from datetime import datetime


class Bank:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename):
            return {"accounts": {}}

        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"accounts": {}}

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4)

    def generate_account_number(self):
        accounts = self.data["accounts"]

        if not accounts:
            return "100001"

        numbers = [int(acc) for acc in accounts.keys()]
        return str(max(numbers) + 1)

    def create_account(self, name, pin, initial_deposit):
        account_number = self.generate_account_number()

        account = {
            "name": name,
            "pin": pin,
            "balance": initial_deposit,
            "transactions": []
        }

        if initial_deposit > 0:
            account["transactions"].append({
                "type": "Account Opening Deposit",
                "amount": initial_deposit,
                "date": self.current_time(),
                "balance": initial_deposit
            })

        self.data["accounts"][account_number] = account
        self.save_data()

        return account_number

    def authenticate(self, account_number, pin):
        account = self.data["accounts"].get(account_number)

        if account and account["pin"] == pin:
            return True

        return False

    def get_account(self, account_number):
        return self.data["accounts"].get(account_number)

    def deposit(self, account_number, amount):
        if amount <= 0:
            return False, "Amount must be greater than zero."

        account = self.get_account(account_number)

        if account is None:
            return False, "Account not found."

        account["balance"] += amount

        account["transactions"].append({
            "type": "Deposit",
            "amount": amount,
            "date": self.current_time(),
            "balance": account["balance"]
        })

        self.save_data()

        return True, f"₹{amount:.2f} deposited successfully."

    def withdraw(self, account_number, amount):
        if amount <= 0:
            return False, "Amount must be greater than zero."

        account = self.get_account(account_number)

        if account is None:
            return False, "Account not found."

        if amount > account["balance"]:
            return False, "Insufficient balance."

        account["balance"] -= amount

        account["transactions"].append({
            "type": "Withdrawal",
            "amount": amount,
            "date": self.current_time(),
            "balance": account["balance"]
        })

        self.save_data()

        return True, f"₹{amount:.2f} withdrawn successfully."

    def transfer(self, sender_number, receiver_number, amount):
        if amount <= 0:
            return False, "Amount must be greater than zero."

        if sender_number == receiver_number:
            return False, "Cannot transfer money to the same account."

        sender = self.get_account(sender_number)
        receiver = self.get_account(receiver_number)

        if sender is None:
            return False, "Sender account not found."

        if receiver is None:
            return False, "Receiver account not found."

        if amount > sender["balance"]:
            return False, "Insufficient balance."

        sender["balance"] -= amount
        receiver["balance"] += amount

        current_time = self.current_time()

        sender["transactions"].append({
            "type": "Transfer Sent",
            "to": receiver_number,
            "amount": amount,
            "date": current_time,
            "balance": sender["balance"]
        })

        receiver["transactions"].append({
            "type": "Transfer Received",
            "from": sender_number,
            "amount": amount,
            "date": current_time,
            "balance": receiver["balance"]
        })

        self.save_data()

        return True, f"₹{amount:.2f} transferred successfully."

    def change_pin(self, account_number, old_pin, new_pin):
        account = self.get_account(account_number)

        if account is None:
            return False, "Account not found."

        if account["pin"] != old_pin:
            return False, "Incorrect current PIN."

        if len(new_pin) != 4 or not new_pin.isdigit():
            return False, "New PIN must contain exactly 4 digits."

        account["pin"] = new_pin
        self.save_data()

        return True, "PIN changed successfully."

    def current_time(self):
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")