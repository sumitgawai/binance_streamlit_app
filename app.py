import time
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from data_ingestion import start_ws
from resampler import resample_ticks
from analytics import compute_spread, zscore, rolling_corr, adf_test
from alerts import check_zscore_alert
from state import STATE

st.set_page_config(layout="wide")
st.title("Real-Time Quant Trading Analytics")

symbols = st.multiselect(
    "Select symbols",
    ["BTCUSDT", "ETHUSDT", "BNBUSDT"],
    default=["BTCUSDT", "ETHUSDT"]
)

timeframe = st.selectbox("Timeframe", ["1s", "1m", "5m"])
window = st.slider("Rolling Window", 10, 200, 50)
z_thresh = st.slider("Z-Score Alert Threshold", 0.5, 3.0, 2.0)

if "ws_started" not in st.session_state:
    start_ws(symbols)
    st.session_state.ws_started = True

resample_ticks()

bars = STATE.bars.get(timeframe)
if isinstance(bars, pd.DataFrame) and len(bars) > 0:
    sym1, sym2 = symbols[:2]
    spread, beta = compute_spread(bars, sym1, sym2)
    z = zscore(spread, window)
    corr = rolling_corr(bars, sym1, sym2, window)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=spread.index, y=spread, name="Spread"))
    st.plotly_chart(fig, use_container_width=True)

    fig_z = go.Figure()
    fig_z.add_trace(go.Scatter(x=z.index, y=z, name="Z-Score"))
    fig_z.add_hline(y=z_thresh, line_dash="dash")
    fig_z.add_hline(y=-z_thresh, line_dash="dash")
    st.plotly_chart(fig_z, use_container_width=True)

    if check_zscore_alert(z.iloc[-1], z_thresh):
        st.error("Z-Score Alert Triggered")

    if st.button("Run ADF Test"):
        st.json(adf_test(spread))

    st.download_button(
        "Download Spread CSV",
        spread.to_csv().encode(),
        "spread.csv"
    )

st.caption("Live data updates automatically")
time.sleep(1)
st.rerun()
