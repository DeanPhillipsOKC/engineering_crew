
class TransactionManager:
    def __init__(self):
        # List of transactions, each transaction is a dict (e.g., {'symbol': 'AAPL', 'quantity': 5, 'price': 100})
        self.transactions = []

    def add_transaction(self, symbol, quantity, price):
        # Adds a buy/sell transaction (buy if quantity>0, sell if quantity<0)
        self.transactions.append({
            'symbol': symbol,
            'quantity': quantity,
            'price': price
        })

    def get_transactions(self, symbol=None):
        # Returns transaction history, optionally filtered by symbol
        if symbol:
            return [tx for tx in self.transactions if tx['symbol'] == symbol]
        return list(self.transactions)


class PortfolioManager:
    def __init__(self, transaction_manager=None):
        # transaction_manager is a reference to the TransactionManager instance
        self.transaction_manager = transaction_manager

    def update_transaction_manager(self, transaction_manager):
        # Updates the reference to a TransactionManager instance
        self.transaction_manager = transaction_manager

    def get_holdings(self):
        # Computes current holdings by aggregating transaction history
        # Returns dict {symbol: total_quantity}
        if not self.transaction_manager:
            raise RuntimeError('TransactionManager reference is not set')
        holdings = {}
        for tx in self.transaction_manager.get_transactions():
            symbol = tx['symbol']
            holdings[symbol] = holdings.get(symbol, 0) + tx['quantity']
        return holdings

    def get_portfolio_value(self, price_lookup):
        # price_lookup is a dict {symbol: current_price}
        # Returns the current total value of portfolio
        holdings = self.get_holdings()
        return sum(holdings[symbol] * price_lookup.get(symbol, 0) for symbol in holdings)