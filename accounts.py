# accounts.py
import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from collections import defaultdict
import bisect

# 1. get_share_price function with fixed prices for AAPL, TSLA, GOOGL

def get_share_price(symbol: str) -> float:
    prices = {
        'AAPL': 175.00,
        'TSLA': 700.00,
        'GOOGL': 2750.00
    }
    return prices.get(symbol.upper(), 100.0)  # Default price for unlisted symbols

# 2. Transaction dataclass
@dataclass
class Transaction:
    timestamp: datetime.datetime
    type: str  # deposit, withdraw, buy, sell
    amount: Optional[float] = None  # for deposit/withdraw
    symbol: Optional[str] = None  # for buy/sell
    quantity: Optional[int] = None  # for buy/sell
    price: Optional[float] = None  # for buy/sell (price per share)
    balance_after: float = 0.0
    holdings_after: Dict[str, int] = field(default_factory=dict)

    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'type': self.type,
            'amount': self.amount,
            'symbol': self.symbol,
            'quantity': self.quantity,
            'price': self.price,
            'balance_after': self.balance_after,
            'holdings_after': self.holdings_after.copy()
        }

# 3. Account class
class Account:
    def __init__(self, username: str):
        self.username = username
        self._balance = 0.0
        self._holdings = defaultdict(int)  # symbol -> quantity
        self._transactions: List[Transaction] = []
        self._initial_deposit = 0.0

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        if len(self._transactions) == 0:
            # First deposit only
            self._initial_deposit = amount
        txn = Transaction(
            timestamp=datetime.datetime.now(),
            type="deposit",
            amount=amount,
            balance_after=self._balance,
            holdings_after=self._holdings.copy()
        )
        self._transactions.append(txn)

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient balance for withdrawal.")
        # Check available funds after withdrawal don't drop below reserved in shares
        # All share values are 'locked' unless user sells them
        self._balance -= amount
        txn = Transaction(
            timestamp=datetime.datetime.now(),
            type="withdraw",
            amount=amount,
            balance_after=self._balance,
            holdings_after=self._holdings.copy()
        )
        self._transactions.append(txn)

    def buy_shares(self, symbol: str, quantity: int):
        if quantity <= 0:
            raise ValueError("Buy quantity must be positive.")
        symbol = symbol.upper()
        price = get_share_price(symbol)
        total_cost = price * quantity
        if total_cost > self._balance:
            raise ValueError(
                f"Not enough balance to buy {quantity} shares of {symbol} at ${price:.2f} each."
            )
        self._balance -= total_cost
        self._holdings[symbol] += quantity
        txn = Transaction(
            timestamp=datetime.datetime.now(),
            type="buy",
            symbol=symbol,
            quantity=quantity,
            price=price,
            amount=total_cost, # total amount spent for transaction
            balance_after=self._balance,
            holdings_after=self._holdings.copy()
        )
        self._transactions.append(txn)

    def sell_shares(self, symbol: str, quantity: int):
        if quantity <= 0:
            raise ValueError("Sell quantity must be positive.")
        symbol = symbol.upper()
        if self._holdings[symbol] < quantity:
            raise ValueError(f"Not enough shares to sell: {symbol}")
        price = get_share_price(symbol)
        total_proceeds = price * quantity
        self._holdings[symbol] -= quantity
        self._balance += total_proceeds
        txn = Transaction(
            timestamp=datetime.datetime.now(),
            type="sell",
            symbol=symbol,
            quantity=quantity,
            price=price,
            amount=total_proceeds, # total amount received for transaction
            balance_after=self._balance,
            holdings_after=self._holdings.copy()
        )
        self._transactions.append(txn)

    def get_balance(self) -> float:
        return self._balance

    def get_holdings(self) -> Dict[str, int]:
        return dict((k, v) for k, v in self._holdings.items() if v > 0)

    def get_portfolio_value(self) -> float:
        value = 0.0
        for symbol, qty in self._holdings.items():
            if qty > 0:
                price = get_share_price(symbol)
                value += price * qty
        return value

    def get_total_value(self) -> float:
        return self._balance + self.get_portfolio_value()

    def get_profit_loss(self) -> float:
        """
        Returns P/L vs initial deposit (if no deposit -> return 0)
        """
        if self._initial_deposit == 0:
            return 0.0
        return self.get_total_value() - self._initial_deposit

    def get_transaction_history(self) -> List[Transaction]:
        return list(self._transactions)

    def _find_transactions_before(self, timestamp: datetime.datetime) -> int:
        # Binary search for largest index with timestamp <= given
        lo, hi = 0, len(self._transactions)
        while lo < hi:
            mid = (lo + hi) // 2
            if self._transactions[mid].timestamp <= timestamp:
                lo = mid + 1
            else:
                hi = mid
        return lo  # Num of txns with timestamp <= given

    def get_holdings_at(self, timestamp: datetime.datetime) -> Dict[str, int]:
        holdings = defaultdict(int)
        txns = self._transactions
        for txn in txns:
            if txn.timestamp > timestamp:
                break
            if txn.type == 'buy' and txn.symbol and txn.quantity:
                holdings[txn.symbol] += txn.quantity
            elif txn.type == 'sell' and txn.symbol and txn.quantity:
                holdings[txn.symbol] -= txn.quantity
        return dict((k, v) for k, v in holdings.items() if v > 0)

    def _balance_and_holdings_at(self, timestamp: datetime.datetime) -> (float, Dict[str, int]):
        balance = 0.0
        holdings = defaultdict(int)
        first_deposit_done = False
        for txn in self._transactions:
            if txn.timestamp > timestamp:
                break
            if txn.type == 'deposit' and txn.amount:
                balance += txn.amount
                if not first_deposit_done:
                    first_deposit_done = True
            elif txn.type == 'withdraw' and txn.amount:
                balance -= txn.amount
            elif txn.type == 'buy' and txn.symbol and txn.quantity and txn.price is not None:
                total_cost = txn.price * txn.quantity
                balance -= total_cost
                holdings[txn.symbol] += txn.quantity
            elif txn.type == 'sell' and txn.symbol and txn.quantity and txn.price is not None:
                total_proceeds = txn.price * txn.quantity
                holdings[txn.symbol] -= txn.quantity
                balance += total_proceeds
        return balance, dict((k, v) for k, v in holdings.items() if v > 0)

    def get_portfolio_value_at(self, timestamp: datetime.datetime) -> float:
        _, holdings = self._balance_and_holdings_at(timestamp)
        value = 0.0
        for symbol, qty in holdings.items():
            if qty > 0:
                price = get_share_price(symbol)
                value += price * qty
        return value

    def get_total_value_at(self, timestamp: datetime.datetime) -> float:
        balance, holdings = self._balance_and_holdings_at(timestamp)
        value = balance
        for symbol, qty in holdings.items():
            if qty > 0:
                price = get_share_price(symbol)
                value += price * qty
        return value

    def get_profit_loss_at(self, timestamp: datetime.datetime) -> float:
        # Find initial deposit up to timestamp
        init_deposit = 0.0
        for txn in self._transactions:
            if txn.type == 'deposit':
                if txn.timestamp <= timestamp:
                    init_deposit += txn.amount if txn.amount is not None else 0.0
        if not init_deposit:
            return 0.0
        return self.get_total_value_at(timestamp) - init_deposit

    def get_transaction_history_at(self, timestamp: datetime.datetime) -> List[Transaction]:
        return [txn for txn in self._transactions if txn.timestamp <= timestamp]

# Example/Test Usage
if __name__ == "__main__":
    import time
    acc = Account(username="alice")
    print("Initial Balance:", acc.get_balance())
    acc.deposit(10000)
    print("Balance after deposit:", acc.get_balance())
    acc.buy_shares("AAPL", 10)
    print("Balance after buying 10 AAPL:", acc.get_balance())
    print("Holdings:", acc.get_holdings())
    print("Portfolio value:", acc.get_portfolio_value())
    print("Total value:", acc.get_total_value())
    print("Profit/Loss:", acc.get_profit_loss())
    # Delay for timestamps
    t_snapshot = datetime.datetime.now()
    time.sleep(0.1)
    acc.deposit(3000)
    acc.buy_shares("TSLA", 2)
    acc.sell_shares("AAPL", 3)
    acc.withdraw(1000)
    print("\nHoldings at snapshot:", acc.get_holdings_at(t_snapshot))
    print("P/L at snapshot:", acc.get_profit_loss_at(t_snapshot))
    print("Transactions at snapshot:")
    for t in acc.get_transaction_history_at(t_snapshot):
        print(t.to_dict())
    print("\nFull transaction history:")
    for t in acc.get_transaction_history():
        print(t.to_dict())
    try:
        acc.withdraw(100000)
    except Exception as e:
        print("Expected withdrawal error:", e)
    try:
        acc.buy_shares("GOOGL", 9999)
    except Exception as e:
        print("Expected buy error:", e)
    try:
        acc.sell_shares("AAPL", 99)
    except Exception as e:
        print("Expected sell error:", e)
