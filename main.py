from bank import Bank


bank = Bank()


def line():
    print("=" * 50)


def welcome():
    line()
    print("             PYTHON VAULT")
    print("      CLI ATM & BANK SIMULATOR")
    line()


def get_amount():
    while True:
        try:
            amount = float(input("Enter amount: ₹"))

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            return amount

        except ValueError:
            print("Invalid amount. Please enter a number.")


def create_account():
    print("\n========== CREATE ACCOUNT ==========")

    name = input("Enter your full name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    while True:
        pin = input("Create a 4-digit PIN: ")

        if len(pin) == 4 and pin.isdigit():
            break

        print("PIN must contain exactly 4 digits.")

    print("\nEnter initial deposit.")
    initial_deposit = get_amount()

    account_number = bank.create_account(
        name,
        pin,
        initial_deposit
    )

    print("\nAccount created successfully!")
    print(f"Account Holder : {name}")
    print(f"Account Number : {account_number}")
    print(f"Initial Balance: ₹{initial_deposit:.2f}")

    print("\nIMPORTANT: Remember your account number and PIN.")


def login():
    print("\n========== LOGIN ==========")

    account_number = input("Enter account number: ").strip()

    attempts = 3

    while attempts > 0:

        pin = input("Enter 4-digit PIN: ")

        if bank.authenticate(account_number, pin):
            print("\nLogin successful!")

            account = bank.get_account(account_number)
            print(f"Welcome, {account['name']}!")

            atm_menu(account_number)
            return

        attempts -= 1

        if attempts > 0:
            print(f"Incorrect account number or PIN.")
            print(f"Attempts remaining: {attempts}")
        else:
            print("Too many failed attempts.")
            print("Returning to main menu.")


def check_balance(account_number):
    account = bank.get_account(account_number)

    print("\n========== BALANCE ==========")
    print(f"Available Balance: ₹{account['balance']:.2f}")


def deposit_money(account_number):
    print("\n========== DEPOSIT ==========")

    amount = get_amount()

    success, message = bank.deposit(
        account_number,
        amount
    )

    print(message)


def withdraw_money(account_number):
    print("\n========== WITHDRAW ==========")

    amount = get_amount()

    success, message = bank.withdraw(
        account_number,
        amount
    )

    print(message)


def transfer_money(account_number):
    print("\n========== MONEY TRANSFER ==========")

    receiver = input(
        "Enter receiver account number: "
    ).strip()

    amount = get_amount()

    success, message = bank.transfer(
        account_number,
        receiver,
        amount
    )

    print(message)


def transaction_history(account_number):
    account = bank.get_account(account_number)

    print("\n========== TRANSACTION HISTORY ==========")

    transactions = account["transactions"]

    if not transactions:
        print("No transactions available.")
        return

    for i, transaction in enumerate(transactions, start=1):

        print(f"\nTransaction {i}")
        print(f"Type   : {transaction['type']}")
        print(f"Amount : ₹{transaction['amount']:.2f}")
        print(f"Date   : {transaction['date']}")

        if "to" in transaction:
            print(f"To     : {transaction['to']}")

        if "from" in transaction:
            print(f"From   : {transaction['from']}")

        print(
            f"Balance: ₹{transaction['balance']:.2f}"
        )


def change_pin(account_number):
    print("\n========== CHANGE PIN ==========")

    old_pin = input("Enter current PIN: ")
    new_pin = input("Enter new 4-digit PIN: ")

    success, message = bank.change_pin(
        account_number,
        old_pin,
        new_pin
    )

    print(message)


def atm_menu(account_number):

    while True:

        print("\n")
        line()
        print("                 ATM MENU")
        line()

        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            check_balance(account_number)

        elif choice == "2":
            deposit_money(account_number)

        elif choice == "3":
            withdraw_money(account_number)

        elif choice == "4":
            transfer_money(account_number)

        elif choice == "5":
            transaction_history(account_number)

        elif choice == "6":
            change_pin(account_number)

        elif choice == "7":
            print("\nLogged out successfully.")
            break

        else:
            print("\nInvalid choice. Please select 1-7.")


def main():

    while True:

        welcome()

        print("\n1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            create_account()

        elif choice == "2":
            login()

        elif choice == "3":
            print("\nThank you for using Python Vault!")
            print("Goodbye.")
            break

        else:
            print("\nInvalid choice. Please select 1-3.")


if __name__ == "__main__":
    main()