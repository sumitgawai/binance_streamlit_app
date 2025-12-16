import pandas as pd
from state import STATE

TIMEFRAMES = {
    "1s": "1S",
    "1m": "1min",
    "5m": "5min",
}

def resample_ticks():
    with STATE.lock:
        if not STATE.ticks:
            return

        df = pd.DataFrame(list(STATE.ticks))
        df.set_index("timestamp", inplace=True)

    for tf, rule in TIMEFRAMES.items():
        bars = (
            df.groupby("symbol")
            .resample(rule)
            .agg(
                open=("price", "first"),
                high=("price", "max"),
                low=("price", "min"),
                close=("price", "last"),
                volume=("qty", "sum"),
            )
            .dropna()
            .reset_index()
        )
        STATE.bars[tf] = bars
