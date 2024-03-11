from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    """
    A hypothetical trading strategy targeting the TQQQ ETF,
    attempting to capture swings in momentum based on RSI and SMA indicators.
    Please note: This strategy is purely illustrative and does not guarantee any return.
    """

    @property
    def assets(self):
        # Targeting the TQQQ ETF
        return ["TQQQ"]

    @property
    def interval(self):
        # Using daily intervals for analysis
        return "1day"

    def run(self, data):
        """
        The core logic of the strategy, analyzing RSI for overbought/oversold conditions,
        and using SMA for trend direction.
        """
        # Initialize the stake in TQQQ to be 0 initially
        tqqq_stake = 0

        # Retrieve the daily closing prices for TQQQ
        close_prices = [i["TQQQ"]["close"] for i in data["ohlcv"] if "TQQQ" in i]

        # Calculate the RSI with a window of 14 days
        rsi_values = RSI("TQQQ", data["ohlcv"], 14)

        # Calculate the Short-term (10 days) and Long-term (30 days) SMA
        short_sma = SMA("TQQQ", data["ohlcv"], 10)
        long_sma = SMA("TQQQ", data["ohlcv"], 30)

        if len(rsi_values) > 0 and len(short_sma) > 0 and len(long_sma) > 0:
            # Most recent RSI and SMA values
            current_rsi = rsi_values[-1]
            current_short_sma = short_sma[-1]
            current_long_sma = long_sma[-1]

            # Conditions for entering a position in TQQQ
            # Entry Condition: RSI below 30 (oversold) and Short-term SMA above Long-term SMA (uptrend)
            if current_rsi < 30 and current_short_sma > current_long_sma:
                log("Buying Signal: RSI indicates oversold, and SMA indicates uptrend.")
                tqqq_stake = 1  # Full allocation to TQQQ

            # Exit Condition: RSI above 70 (overbought)
            elif current_rsi > 70:
                log("Selling Signal: RSI indicates overbought.")
                tqqq_stake = 0  # Exiting TQQQ position

        return TargetAllocation({"TQQQ": tqqq_stake})