from .base_pattern import BasePattern
from typing import List
from ...candlestick import CandleStick

class MorningStarNoGap(BasePattern):
    """
    Class for an morning star pattern.
    """

    def __init__(self, candlesticks: List[CandleStick]):
        """
        Initializes the morning Star pattern.
        """
        super().__init__(candlesticks)
        self.candlesticks = candlesticks
        self.trend = "bullish"
        self.pattern_name = "MorningStarNoGap"
        self.no_candles = 3

    def run(self):
        """
        Runs the morning Star pattern.

        Return:
            list[int]: index of the candlestick where the morning Star pattern was found
        """
        assert len(self.candlesticks) > 2, "There must be at least 3 candlesticks to run the morning Star pattern"
        found_positions = []

        candlestick_0 = None
        candlestick_1 = None
        candlestick_2 = None

        dp = [0] * len(self.candlesticks)
        for i in range(len(self.candlesticks)):
            if i == 0:
                dp[i] = abs(self.candlesticks[i].close - self.candlesticks[i].open)
            else:
                dp[i] = abs(self.candlesticks[i].close - self.candlesticks[i].open) + dp[i - 1]

        for i in range(len(self.candlesticks) - 2):
            candlestick_0 = self.candlesticks[i]
            candlestick_1 = self.candlesticks[i + 1]
            candlestick_2 = self.candlesticks[i + 2]
            
            body_0 = abs(candlestick_0.close - candlestick_0.open)
            body_1 = abs(candlestick_1.close - candlestick_1.open)
            body_2 = abs(candlestick_2.close - candlestick_2.open)

            min_idx = i - 22 if i >= 22 else 0
            average_body = (dp[i] - dp[min_idx]) / (i - min_idx + 1)

            # First day A tall black candle.
            # Second day A small-bodied candle that gaps lower from the prior body. The
            # color can be either black or white.
            # Third day A tall white candle that gaps above the body of the second day
            # and closes at least midway into the black body of the first day.
            
            # candlestick_0 is black and tall
            if candlestick_0.close < candlestick_0.open and body_0 >= average_body:
                if candlestick_1.close <= candlestick_1.open:
                    if body_2 >= average_body and \
                        candlestick_2.close > candlestick_2.open and \
                        candlestick_2.open >= candlestick_1.close and \
                        candlestick_2.close > candlestick_0.open - (candlestick_0.open - candlestick_0.close) / 2:
                        found_positions.append(i + 2)

        return found_positions

    def __repr__(self) -> str:
        return "Morning Star Pattern"

            
            