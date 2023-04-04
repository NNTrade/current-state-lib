from NNTrade.indicators.indicator_settings import IndicatorSettings
from .indicator_current_state import IndicatorCurrentState
from typing import Dict


class ChartIndicatorCurrentState:
    def __init__(self, indicators_current_states: Dict[IndicatorSettings, IndicatorCurrentState]) -> None:
        super().__init__()
        self._indicators_cs = indicators_current_states

    def get(self, indicator_cfg: IndicatorSettings) -> IndicatorCurrentState:
        return self._indicators_cs[indicator_cfg]

    def get_all(self) -> Dict[IndicatorSettings, IndicatorCurrentState]:
        return self._indicators_cs.copy()

    def __str__(self) -> str:
        return self._indicators_cs.__str__()
