import tkinter as tk
from tkinter import messagebox

class InvalidInputError(Exception):
    pass

class TransferError(Exception):
    pass

def process_user_input(bank, choice):
    if choice == "1":
        account_type = input("Select account type (1 for Personal, 2 for Business): ")
        if account_type == "1":
            account = bank.create_account("Personal")
        elif account_type == "2":
            account = bank.create_account("Business")
        else:
            print("Unsupported account type")
            return
        print(f"Account created. Account id: {account.account_id}, Passcode: {account.passcode}")

    elif choice == "2":
        account_id = input("Enter your account id: ")
        passcode = input("Enter your passcode: ")
        account = bank.login(account_id, passcode)
        try:
            while True:
                print("\n1. Check funds\n2. Deposit\n3. Withdraw\n4. Transfer\n5. Top-Up Mobile\n6. Delete Account\n7. Logout")
                action = input("Enter your choice: ")

                if action == "1":
                    print(f"Your funds is {account.funds}")

                elif action == "2":
                    try:
                        amount = float(input("Please input the deposit amount: "))
                        print(account.deposit(amount))
                        bank.save_accounts()
                    except ValueError:
                        raise InvalidInputError("Deposit amount must be a number.")

                elif action == "3":
                    try:
                        amount = float(input("Please input the withdrawal amount: "))
                        print(account.withdraw(amount))
                        bank.save_accounts()
                    except ValueError:
                        raise InvalidInputError("Withdrawal amount must be a number.")

                elif action == "4":
                    recipient_id = input("Enter recipient account id: ")
                    try:
                        amount = float(input("Enter amount to transfer: "))
                        recipient_account = bank.accounts[recipient_id]
                        print(account.transfer(amount, recipient_account))
                        bank.save_accounts()
                    except KeyError:
                        raise TransferError("Recipient account does not exist.")
                    except ValueError:
                        raise InvalidInputError("Transfer amount must be a number.")

                elif action == "5":
                    number = input("Enter mobile number: ")
                    try:
                        amount = float(input("Enter top-up amount: "))
                        print(account.withdraw(amount))
                        print(f"Successfully topped up {amount} to mobile number {number}.")
                        bank.save_accounts()
                    except ValueError:
                        raise InvalidInputError("Top-up amount must be a number.")

                elif action == "6":
                    bank.delete_account(account_id)
                    print("Account deletion successful")
                    break

                elif action == "7":
                    break
                else:
                    print("Please select a valid option.")

        except (InvalidInputError, TransferError) as e:
            print(e)

    elif choice == "3":
        exit()
    else:
        print("Please select a valid option..")
class BankingSystem:
    def __init__(self):
        self.accounts = {} 
        print("Banking system initialized.")
    def create_account(self, account_type):
        account = Account(account_type)
        self.accounts[account.account_id] = account
        return account
    def delete_account(self, account_id):
        if account_id in self.accounts:
            del self.accounts[account_id]
            return True
        else:
            return False
    
class Account:
    _id_counter = 1 
    def __init__(self, account_type):
        self.account_id = str(Account._id_counter)  # Unique account ID as a string
        Account._id_counter += 1
        self.account_type = account_type
        self.funds = 0 
    def deposit(self, amount):
        self.funds += amount
        return f"Deposited {amount}. New balance: {self.funds}"
    def withdraw(self, amount):
        if amount > self.funds:
            return "Insufficient funds"
        self.funds -= amount
        return f"Withdrew {amount}. New balance: {self.funds}"
    def transfer(self, amount, recipient_account):
        if amount > self.funds:
            raise TransferError("Insufficient funds for transfer.")
        self.funds -= amount
        recipient_account.funds += amount
        return f"Transferred {amount} to account {recipient_account.account_id}. New balance: {self.funds}"

def main():
    bank = BankingSystem()
    while True:
        print("\nHello. How can I assist you?\n1. Open Account\n2. Login to your Account\n3. Exit")
        choice = input("Enter your choice: ")
        process_user_input(bank, choice)


class BankingGUI:
    def __init__(self, master):
        self.bank = BankingSystem()
        self.master = master
        master.title("Banking System")

        self.label = tk.Label(master, text="Select an option:")
        self.label.pack()

        self.open_btn = tk.Button(master, text="Open Account", command=self.open_account)
        self.open_btn.pack()

        self.login_btn = tk.Button(master, text="Login", command=self.login)
        self.login_btn.pack()

        self.exit_btn = tk.Button(master, text="Exit", command=master.quit)
        self.exit_btn.pack()

    def open_account(self):
        account_type = input("Select account type (1 for Personal, 2 for Business): ")
        if account_type == "1":
            account = self.bank.create_account("Personal")
        elif account_type == "2":
            account = self.bank.create_account("Business")
        else:
            messagebox.showinfo("Info", "Unsupported account type")
            return
        messagebox.showinfo("Info", f"Account created. ID: {account.account_id}, Passcode: {account.passcode}")

    def login(self):
        account_id = input("Enter your account id: ")
        passcode = input("Enter your passcode: ")
        try:
            account = self.bank.login(account_id, passcode)
            messagebox.showinfo("Success", f"Login successful. Your balance is {account.funds}")
        except:
            messagebox.showinfo("Error", "Login failed")

if __name__ == "__main__":
    main()
