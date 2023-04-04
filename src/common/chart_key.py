from __future__ import annotations
from NNTrade.common.time_frame import TimeFrame
from NNTrade.indicators.const_hash import const_hash


class ChartKey:
    def __init__(self, stock: str, timeframe: TimeFrame) -> None:
        self.__stock = stock
        self.__timeframe = timeframe
        self._hash = const_hash(self.__stock) * hash(self.timeframe.value)
        pass

    @property
    def stock(self) -> str:
        return self.__stock

    @property
    def timeframe(self) -> TimeFrame:
        return self.__timeframe

    def __eq__(self, other: ChartKey):
        return isinstance(other, ChartKey) and \
            self.stock == other.stock and \
            self.timeframe == other.timeframe

    def __hash__(self):
        return self._hash
