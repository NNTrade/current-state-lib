from abc import ABC, abstractmethod, abstractproperty
from typing import Dict, List
import pandas as pd
import sys


class IndicatorCurrentState(ABC):
    @abstractmethod
    def value(self, name: str) -> float:
        ...

    @property
    @abstractproperty
    def values(self) -> Dict[str, value]:
        ...

    def __str__(self) -> str:
        return self.values.__str__()


class IndicatorCurrentStateConatiner(IndicatorCurrentState):
    def __init__(self, indicator_df: pd.DataFrame, clean_up_period: int = sys.maxsize) -> None:
        super().__init__()
        self.__ind_val_dic: List[Dict[str, float]
                                 ] = indicator_df.shift(1).to_dict('records')
        self.__cur_idx = -1
        self.__keys: List[str] = indicator_df.columns
        self._cur_val: Dict[str:float] = {k: None for k in self.__keys}
        self._clean_up_period = clean_up_period
        pass

    def value(self, name: str) -> float:
        return self._cur_val[name]

    @property
    def values(self) -> Dict[str, value]:
        return self._cur_val.copy()

    def next(self):
        self.__cur_idx = self.__cur_idx + 1
        if self.__cur_idx > self._clean_up_period:
            self.__ind_val_dic = self.__ind_val_dic[self.__cur_idx:]
            self.__cur_idx = 0
        self._cur_val = self.__ind_val_dic[self.__cur_idx]
