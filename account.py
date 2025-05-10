class Account:
    def __init__(self, account_id, owner, initial_balance=0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self.account_id = account_id
        self.owner = owner
        self.balance = float(initial_balance)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive.")
        if self.balance - amount < 0:
            raise ValueError("Insufficient funds. Cannot have negative balance.")
        self.balance -= amount
        return self.balance

    def get_balance(self):
        return self.balance

class AccountManager:
    def __init__(self):
        self._accounts = {}
        self._next_id = 1

    def create_account(self, owner, initial_balance=0.0):
        if not owner or not isinstance(owner, str):
            raise ValueError("Owner name is required and must be a string.")
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        account_id = self._next_id
        if account_id in self._accounts:
            raise RuntimeError("Account ID already exists. This should not happen.")
        account = Account(account_id, owner, initial_balance)
        self._accounts[account_id] = account
        self._next_id += 1
        return account_id

    def deposit(self, account_id, amount):
        account = self._get_account(account_id)
        return account.deposit(amount)

    def withdraw(self, account_id, amount):
        account = self._get_account(account_id)
        return account.withdraw(amount)

    def get_balance(self, account_id):
        account = self._get_account(account_id)
        return account.get_balance()

    def get_account(self, account_id):
        return self._get_account(account_id)

    def _get_account(self, account_id):
        if account_id not in self._accounts:
            raise ValueError(f"Account with ID {account_id} does not exist.")
        return self._accounts[account_id]
