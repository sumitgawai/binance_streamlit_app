import numpy as np
import pandas as pd
from statsmodels.regression.linear_model import OLS
from statsmodels.tsa.stattools import adfuller

def hedge_ratio(y, x):
    x = np.asarray(x)
    y = np.asarray(y)
    x = sm.add_constant(x)
    model = OLS(y, x).fit()
    return model.params[1]

def compute_spread(df, sym1, sym2):
    prices = df.pivot(index="timestamp", columns="symbol", values="close").dropna()
    y = prices[sym1]
    x = prices[sym2]
    beta = np.polyfit(x, y, 1)[0]
    spread = y - beta * x
    return spread, beta

def zscore(series, window):
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    return (series - mean) / std

def rolling_corr(df, sym1, sym2, window):
    prices = df.pivot(index="timestamp", columns="symbol", values="close").dropna()
    return prices[sym1].rolling(window).corr(prices[sym2])

def adf_test(series):
    result = adfuller(series.dropna())
    return {
        "ADF Statistic": result[0],
        "p-value": result[1]
    }
