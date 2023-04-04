from __future__ import annotations
from ..common import ChartKey
from NNTrade.indicators.indicator_settings import IndicatorSettings
from .indicator_current_state import IndicatorCurrentState, IndicatorCurrentStateConatiner
from .chart_indicators_current_state import ChartIndicatorCurrentState
from typing import Dict, Tuple


class MarketIndicatorsCurrentState:
    @staticmethod
    def build_from_dict_tupl_cnt(tuple_cnt_dict: Dict[Tuple[ChartKey, IndicatorSettings], IndicatorCurrentStateConatiner]) -> MarketIndicatorsCurrentState:
        ck_dict: Dict[ChartKey, Dict[IndicatorSettings,
                                     IndicatorCurrentStateConatiner]] = {}

        for k, v in tuple_cnt_dict.items():
            ind_cfg_dict = ck_dict.pop(k[0], {})
            ind_cfg_dict[k[1]] = v
            ck_dict[k[0]] = ind_cfg_dict

        return MarketIndicatorsCurrentState({k: ChartIndicatorCurrentState(v) for k, v in ck_dict.items()})

    def __init__(self, chart_indicators_current_state: Dict[ChartKey, ChartIndicatorCurrentState]) -> None:
        super().__init__()
        self._chart_indicators_cs: Dict[ChartKey,
                                        ChartIndicatorCurrentState] = chart_indicators_current_state

    def get(self, chart_setting: ChartKey, indicator_cfg: IndicatorSettings) -> IndicatorCurrentState:
        return self._chart_indicators_cs[chart_setting].get(indicator_cfg)

    def get_for(self, chart_setting: ChartKey) -> ChartIndicatorCurrentState:
        return self._chart_indicators_cs[chart_setting]

    def __str__(self) -> str:
        return self._chart_indicators_cs.__str__()
