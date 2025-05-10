class PortfolioManager:
    """
    A minimal PortfolioManager for reference attachment and can_sell logic.
    """
    def __init__(self):
        # user_holdings is a dict of {symbol: quantity}
        self.user_holdings = {}

    def get_holdings(self, symbol):
        return self.user_holdings.get(symbol, 0)

    def update_holdings(self, symbol, qty):
        self.user_holdings[symbol] = qty

    def can_sell(self, symbol, quantity):
        # Only allow selling if user holds enough shares
        return self.get_holdings(symbol) >= quantity


class TransactionManager:
    """
    Handles transactions and validates them via PortfolioManager instance.
    """
    def __init__(self, portfolio_manager=None):
        self.portfolio_manager = portfolio_manager

    def set_portfolio_manager(self, portfolio_manager):
        self.portfolio_manager = portfolio_manager

    def validate_sell(self, symbol, quantity):
        if not self.portfolio_manager:
            raise ValueError('No portfolio manager attached')
        return self.portfolio_manager.can_sell(symbol, quantity)

    def execute_sell(self, symbol, quantity):
        if self.validate_sell(symbol, quantity):
            current = self.portfolio_manager.get_holdings(symbol)
            self.portfolio_manager.update_holdings(symbol, current - quantity)
            return True
        else:
            return False
