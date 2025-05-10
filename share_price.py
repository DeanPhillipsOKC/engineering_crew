from datetime import datetime
from typing import Optional

class SharePriceProvider:
    """
    Provides share price lookup functionality for tickers.
    Uses stubbed data for known test tickers.
    """
    # Stub price data for test tickers
    _STUB_TICKER_PRICES = {
        'TEST1': 100.25,
        'TEST2': 200.0,
        'MOCK': 42.42,
    }
    _STUB_PRICE_HISTORY = {
        'TEST1': [
            # Tuple of (datetime, price), order does not matter for stub
            (datetime(2024, 1, 1, 14, 0), 99.5),
            (datetime(2024, 6, 1, 10, 0), 100.25),
            (datetime(2024, 1, 1, 9, 30), 98.0),
        ],
        'TEST2': [
            (datetime(2024, 1, 1, 14, 0), 190.4),
            (datetime(2024, 6, 1, 10, 0), 200.0),
        ],
        'MOCK': [
            (datetime(2024, 1, 1, 9, 30), 40.0),
            (datetime(2024, 6, 1, 10, 0), 42.42),
        ],
    }

    def get_price(self, symbol: str) -> float:
        """
        Gets the most recent (stubbed) price for a symbol.
        :param symbol: str ticker symbol
        :return: float price or raises ValueError if not found
        """
        symbol = symbol.upper()
        if symbol in self._STUB_TICKER_PRICES:
            return self._STUB_TICKER_PRICES[symbol]
        raise ValueError(f"No stub price available for symbol: {symbol}")

    def get_price_at_time(self, symbol: str, at_time: datetime) -> Optional[float]:
        """
        Gets the share price at a specific datetime (stub).
        :param symbol: str ticker
        :param at_time: datetime
        :return: float price if exists at exactly that time, else None
        """
        symbol = symbol.upper()
        if symbol not in self._STUB_PRICE_HISTORY:
            return None
        for t, price in self._STUB_PRICE_HISTORY[symbol]:
            if t == at_time:
                return price
        return None
