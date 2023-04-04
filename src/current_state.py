from abc import ABC
from .quote import MarketQuotesCurrentState, StockQuoteCurrentStateContainer
from .datetime_current_state import DateTimeCurrentState, DateTimeCurrentStateConatiner
from .indicator import MarketIndicatorsCurrentState, IndicatorCurrentStateConatiner
import pandas as pd
from typing import Dict, Tuple
import sys
from NNTrade.common.candle_col_name import OPEN
from NNTrade.indicators.indicator_settings import IndicatorSettings
from .common import ChartKey


class CurrentState(ABC):

  @property
  def datetime(self) -> DateTimeCurrentState:
    """Get current state of datetime

    Returns:
        DateTimeCurrentState: Datetime current state
    """
    ...

  @property
  def quotes(self) -> MarketQuotesCurrentState:
    """Get Current state of stock quotes

    Returns:
        MarketQuotesCurrentState: Current state of stock quotes
    """
    ...

  @property
  def indicators(self) -> MarketIndicatorsCurrentState:
    """Get Current state of Indicators 

    Returns:
        MarketIndicatorsCurrentState: Current state of Indicators 
    """
    ...

  @property
  def index(self) -> int:
    """Current index (not datetime)

    Returns:
        int: number if index
    """
    ...

  @property
  def last_index(self) -> int:
    """Last index in datas

    Returns:
        int: last index
    """
    ...

  def __str__(self) -> str:
    return f"index {self.index}, datetime: {self.datetime.__str__()}\nquote: {self.quotes.__str__()},\nindicator {self.indicators.__str__()}"


class CurrentStateContainer(CurrentState):
  def __init__(self, stock_quote_dict: Dict[str, pd.DataFrame],
               indicators_dic: Dict[Tuple[ChartKey, IndicatorSettings], pd.DataFrame],
               clean_up_period: int = sys.maxsize):
    """Contructor
    Use OPEN price and shift indicators values by 1 row to make that indicator does not show data based in CLOSE price of candle which will be in the end of candle.
    
    Args:
        stock_quote_dict (Dict[str, pd.DataFrame]): data of stock quotes
        indicators_dic (Dict[Tuple[ChartKey, IndicatorSettings], pd.DataFrame]): data of stock indicators
        clean_up_period (int, optional): clean up data for decreasing memory requirements. Defaults to sys.maxsize.
    """
    super().__init__()

    self._dt_cs_cnt: DateTimeCurrentStateConatiner = DateTimeCurrentStateConatiner.build_from_dt_sr_arr(
        [*[v.index for v in stock_quote_dict.values()], *[v.index for v in indicators_dic.values()]], clean_up_period)

    sq_cs_cnt_dict = {k: StockQuoteCurrentStateContainer(
        v[OPEN], clean_up_period) for k, v in stock_quote_dict.items()}
    self._market_quotes_cs = MarketQuotesCurrentState(sq_cs_cnt_dict)
    self._sq_cnt_arr = sq_cs_cnt_dict.values()

    ci_cs_cnt_dict: Dict[Tuple[ChartKey, IndicatorSettings], IndicatorCurrentStateConatiner] = {k: IndicatorCurrentStateConatiner(
        v, clean_up_period) for k, v in indicators_dic.items()}
    self._market_indicators_cs = MarketIndicatorsCurrentState.build_from_dict_tupl_cnt(
        ci_cs_cnt_dict)
    self._ind_val_cnt_arr = ci_cs_cnt_dict.values()

    self.__cur_idx = -1
    self._last_index = len([*stock_quote_dict.values()][0].index) - 1

  @property
  def datetime(self) -> DateTimeCurrentState:
    return self._dt_cs_cnt

  @property
  def quotes(self) -> MarketQuotesCurrentState:
    return self._market_quotes_cs

  @property
  def indicators(self) -> MarketIndicatorsCurrentState:
    return self._market_indicators_cs

  @property
  def index(self) -> int:
    return self.__cur_idx

  @property
  def last_index(self) -> int:
    return self._last_index

  def next(self) -> bool:
    """set next state

    Returns:
        bool: is last
    """
    self.__cur_idx = self.__cur_idx + 1

    for sq_cs_cnt in self._sq_cnt_arr:
      sq_cs_cnt.next()

    for ind_val_cnt in self._ind_val_cnt_arr:
      ind_val_cnt.next()
    self._dt_cs_cnt.next()

    return self.__cur_idx == self._last_index
