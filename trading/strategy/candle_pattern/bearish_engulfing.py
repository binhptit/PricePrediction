from .base_pattern import BasePattern
from typing import List
from ...candlestick import CandleStick

class BearishEngulfing(BasePattern):
    """
    Class for an engulfing pattern.
    """

    def __init__(self, candlesticks: List[CandleStick]):
        """
        Initializes the engulfing pattern.
        """
        super().__init__(candlesticks)
        self.candlesticks = candlesticks
        self.trend = "bearish"
        self.pattern_name = "bearish_engulfing"
        self.no_candles = 2

    def run(self):
        """
        Runs the engulfing pattern.

        Return:
            list[int]: index of the candlestick where the engulfing pattern was found
        """
        assert len(self.candlesticks) > 1, "There must be at least 2 candlesticks to run the ThreeLineStrikeBullish pattern"
        found_positions = []

        candlestick_0 = None
        candlestick_1 = None
        candlestick_2 = None
        candlestick_3 = None

        dp = [0] * len(self.candlesticks)
        for i in range(len(self.candlesticks)):
            if i == 0:
                dp[i] = abs(self.candlesticks[i].close - self.candlesticks[i].open)
            else:
                dp[i] = abs(self.candlesticks[i].close - self.candlesticks[i].open) + dp[i - 1]

        for i in range(len(self.candlesticks) - 3):
            candlestick_0 = self.candlesticks[i]
            candlestick_1 = self.candlesticks[i + 1]
            
            upper_shadow_0 = candlestick_0.high - max(candlestick_0.open, candlestick_0.close)
            lower_shadow_0 = min(candlestick_0.open, candlestick_0.close) - candlestick_0.low
            body_0 = abs(candlestick_0.close - candlestick_0.open)

            upper_shadow_1 = candlestick_1.high - max(candlestick_1.open, candlestick_1.close)
            lower_shadow_1 = min(candlestick_1.open, candlestick_1.close) - candlestick_1.low
            body_1 = abs(candlestick_1.close - candlestick_1.open)

            min_idx = i - 22 if i >= 22 else 0
            average_body = (dp[i] - dp[min_idx]) / (i - min_idx + 1)

            # Days 1 to 3 Three white candles, each with a higher close.
            # Last day A black candle that opens higher but closes below the open
            # of the first candle.

            # candlestick_0 must be a bullish candlestick
            if candlestick_0.close < candlestick_0.open:
                continue

            # candlestick_1 must be a bearish candlestick
            if candlestick_1.close > candlestick_1.open:
                continue

            # candlestick_1's body must be bigger than candlestick_0's body
            if body_1 < body_0 or body_1 < average_body:
                continue
                
            found_positions.append(i + 1)

        return found_positions

    def __repr__(self) -> str:
        return "Bearish Engulfing Pattern"

            
            