from abc import ABC, abstractmethod

class SharePriceService(ABC):
    @abstractmethod
    def get_share_price(self, symbol: str) -> float:
        """
        Returns the current price for the given share symbol.
        """
        pass

class InMemorySharePriceService(SharePriceService):
    def __init__(self):
        # Hardcoded prices
        self.prices = {
            'AAPL': 175.00,
            'TSLA': 700.00,
            'GOOGL': 2750.00
        }

    def get_share_price(self, symbol: str) -> float:
        """
        Returns the price for the symbol if set, else returns 100.0
        """
        return self.prices.get(symbol, 100.0)
