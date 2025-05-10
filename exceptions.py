class InsufficientFundsException(Exception):
    """Raised when an account does not have enough funds for a transaction."""
    pass

class InsufficientHoldingsException(Exception):
    """Raised when holdings (e.g., assets or stocks) are insufficient to execute a transaction."""
    pass

class InvalidTransactionException(Exception):
    """Raised when a transaction is invalid due to business logic or rules."""
    pass
