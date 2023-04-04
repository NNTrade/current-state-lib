from __future__ import annotations
from abc import ABC, abstractproperty
from datetime import datetime
import pandas as pd
import sys
from typing import List


class DateTimeCurrentState(ABC):
    @property
    @abstractproperty
    def value(self) -> datetime:
        ...

    def __str__(self) -> str:
        return self.value.__str__()


class DateTimeCurrentStateConatiner(DateTimeCurrentState):
    @staticmethod
    def build_from_dt_sr_arr(dt_sr_arr: List[List[datetime]], clean_up_period: int = sys.maxsize) -> DateTimeCurrentStateConatiner:
        _len = len(dt_sr_arr[0])
        for dt_sr in dt_sr_arr:
            if _len != len(dt_sr):
                raise Exception("Count of index are not equal")

        for i in range(_len):
            _dt = dt_sr_arr[0][i]
            for dt_sr in dt_sr_arr:
                if _dt != dt_sr[i]:
                    raise Exception("Datetimes in all indexes is not equal")

        return DateTimeCurrentStateConatiner(dt_sr_arr[0], clean_up_period)

    def __init__(self, datetime_arr: List[datetime], clean_up_period: int = sys.maxsize) -> None:
        super().__init__()
        self.__datetime_arr = datetime_arr.copy()
        self.__cur_idx = -1
        self._clean_up_period = clean_up_period
        self._cur_dt = None
        pass

    @ property
    def value(self) -> datetime:
        return self._cur_dt

    def next(self):
        self.__cur_idx = self.__cur_idx + 1
        if self.__cur_idx > self._clean_up_period:
            self.__datetime_arr = self.__datetime_arr[self.__cur_idx:]
            self.__cur_idx = 0
        self._cur_dt = self.__datetime_arr[self.__cur_idx]
