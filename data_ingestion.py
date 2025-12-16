import json
import threading
import websocket
from datetime import datetime
from state import STATE

BINANCE_WS = "wss://fstream.binance.com/ws"

def _on_message(ws, message):
    data = json.loads(message)
    tick = {
        "timestamp": datetime.fromtimestamp(data["T"] / 1000),
        "symbol": data["s"],
        "price": float(data["p"]),
        "qty": float(data["q"]),
    }
    with STATE.lock:
        STATE.ticks.append(tick)

def start_ws(symbols):
    streams = "/".join([f"{s.lower()}@trade" for s in symbols])
    ws = websocket.WebSocketApp(
        f"{BINANCE_WS}/{streams}",
        on_message=_on_message,
    )
    t = threading.Thread(target=ws.run_forever, daemon=True)
    t.start()
