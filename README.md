# Current State Lib
Package with classes to store and changing current state of market for simulation

## Import
NNTrade.simulation.current_state @ git+https://git@github.com/NNTrade/current-state-lib.git#egg=NNTrade.simulation.current_state

## Using

```python
from NNTrade.common.time_frame import TimeFrame
from NNTrade.simulation.current_state import CurrentStateContainer, ChartKey

cs_cnt = CurrentStateContainer({"s1": stock1_df, "s2": stock2_df}, {
             (ChartKey("st1", TimeFrame.D), ind1_cfg): ind1_df, (ChartKey("st2", TimeFrame.H), ind2_cfg): ind2_df})

cs_cnt.next()
```