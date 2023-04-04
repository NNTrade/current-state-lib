import unittest
import logging
import pandas as pd
from NNTrade.common.candle_col_name import OPEN
from NNTrade.common.time_frame import TimeFrame
from datetime import datetime
from src.current_state import CurrentStateContainer, ChartKey
from NNTrade.indicators.indicator_settings import IndicatorSettings
import numpy as np


class CurrentStateFactory_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_get_quote_df_THEN_correct(self):
        # Array
        stock1_df = pd.DataFrame({OPEN: [11, 12, 13]}, index=[datetime(
            2020, 1, 1, 1, 1), datetime(2020, 1, 1, 1, 2), datetime(2020, 1, 1, 1, 3)])
        stock2_df = pd.DataFrame({OPEN: [21, 22, 23]}, index=[datetime(
            2020, 1, 1, 1, 1), datetime(2020, 1, 1, 1, 2), datetime(2020, 1, 1, 1, 3)])
        ind1_df = pd.DataFrame({"v11": [101, 102, 103], "v12": [111, 112, 113]}, index=[datetime(
            2020, 1, 1, 1, 1), datetime(2020, 1, 1, 1, 2), datetime(2020, 1, 1, 1, 3)])
        ind2_df = pd.DataFrame({"v21": [201, 202, 203], "v22": [211, 212, 213]}, index=[datetime(
            2020, 1, 1, 1, 1), datetime(2020, 1, 1, 1, 2), datetime(2020, 1, 1, 1, 3)])
        ind1_cfg = IndicatorSettings("ind1", {"a1": 1})
        ind2_cfg = IndicatorSettings("ind2", {"a2": 1})

        # Act 0
        cs_cnt = CurrentStateContainer({"s1": stock1_df, "s2": stock2_df}, {
            (ChartKey("st1", TimeFrame.D), ind1_cfg): ind1_df, (ChartKey("st2", TimeFrame.H), ind2_cfg): ind2_df})

        # Assert 0
        self.assertEqual(2, cs_cnt.last_index)
        self.assertEqual(-1, cs_cnt.index)

        # Act 1
        is_last = cs_cnt.next()

        # Assert 1
        self.assertFalse(is_last)

        self.assertEqual(0, cs_cnt.index)
        self.assertEqual(datetime(2020, 1, 1, 1, 1), cs_cnt.datetime.value)

        self.assertEqual(11, cs_cnt.quotes.get("s1").price)
        self.assertEqual(21, cs_cnt.quotes.get("s2").price)

        self.assertTrue(np.isnan(cs_cnt.indicators.get(
            ChartKey("st1", TimeFrame.D), ind1_cfg).value("v11")))
        self.assertTrue(np.isnan(cs_cnt.indicators.get(
            ChartKey("st1", TimeFrame.D), ind1_cfg).value("v12")))
        self.assertTrue(np.isnan(cs_cnt.indicators.get(
            ChartKey("st2", TimeFrame.H), ind2_cfg).value("v21")))
        self.assertTrue(np.isnan(cs_cnt.indicators.get(
            ChartKey("st2", TimeFrame.H), ind2_cfg).value("v22")))

        # Act 2
        is_last = cs_cnt.next()

        # Assert 2
        self.assertFalse(is_last)

        self.assertEqual(1, cs_cnt.index)
        self.assertEqual(datetime(2020, 1, 1, 1, 2), cs_cnt.datetime.value)

        self.assertEqual(12, cs_cnt.quotes.get("s1").price)
        self.assertEqual(22, cs_cnt.quotes.get("s2").price)

        self.assertEqual(101, cs_cnt.indicators.get(
            ChartKey("st1", TimeFrame.D), ind1_cfg).value("v11"))
        self.assertEqual(111, cs_cnt.indicators.get(
            ChartKey("st1", TimeFrame.D), ind1_cfg).value("v12"))
        self.assertEqual(201, cs_cnt.indicators.get(
            ChartKey("st2", TimeFrame.H), ind2_cfg).value("v21"))
        self.assertEqual(211, cs_cnt.indicators.get(
            ChartKey("st2", TimeFrame.H), ind2_cfg).value("v22"))

        # Act 3
        is_last = cs_cnt.next()

        # Assert 3
        self.assertTrue(is_last)

        self.assertEqual(2, cs_cnt.index)
        self.assertEqual(datetime(2020, 1, 1, 1, 3), cs_cnt.datetime.value)

        self.assertEqual(13, cs_cnt.quotes.get("s1").price)
        self.assertEqual(23, cs_cnt.quotes.get("s2").price)

        self.assertEqual(102, cs_cnt.indicators.get(
            ChartKey("st1", TimeFrame.D), ind1_cfg).value("v11"))
        self.assertEqual(112, cs_cnt.indicators.get(
            ChartKey("st1", TimeFrame.D), ind1_cfg).value("v12"))
        self.assertEqual(202, cs_cnt.indicators.get(
            ChartKey("st2", TimeFrame.H), ind2_cfg).value("v21"))
        self.assertEqual(212, cs_cnt.indicators.get(
            ChartKey("st2", TimeFrame.H), ind2_cfg).value("v22"))
