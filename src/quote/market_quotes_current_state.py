from typing import Dict
from .stock_quote_current_state import StockQuoteCurrentState


class MarketQuotesCurrentState:
    def __init__(self, charts_quotes_current_state: Dict[str, StockQuoteCurrentState]) -> None:
        self._charts_quotes_current_state = charts_quotes_current_state
        pass

    def get(self, stock: str) -> StockQuoteCurrentState:
        return self._charts_quotes_current_state[stock]

    def __str__(self) -> str:
        return self._charts_quotes_current_state.__str__()
