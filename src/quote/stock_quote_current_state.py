from abc import ABC, abstractproperty
import pandas as pd
import sys


class StockQuoteCurrentState(ABC):
    @property
    @abstractproperty
    def price(self) -> float:
        ...

    def __str__(self) -> str:
        return self.price.__str__()


class StockQuoteCurrentStateContainer(StockQuoteCurrentState):
    def __init__(self, quote_sr: pd.Series, clean_up_period: int = sys.maxsize) -> None:
        super().__init__()
        self.__open_arr = quote_sr.to_numpy()
        self.__cur_idx = -1
        self._clean_up_period = clean_up_period
        self._cur_open = None
        pass

    @property
    def price(self) -> float:
        return self._cur_open

    def next(self):
        self.__cur_idx = self.__cur_idx + 1
        if self.__cur_idx > self._clean_up_period:
            self.__open_arr = self.__open_arr[self.__cur_idx:]
            self.__cur_idx = 0
        self._cur_open = self.__open_arr[self.__cur_idx]
