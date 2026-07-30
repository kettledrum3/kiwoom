import asyncio
import websockets
import json
import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from core.cavr import get_access_token

async def test_orig_capital_a():
    market = "US"
    trade_mode = "MOCK"
    token = get_access_token(market, force=True, trade_mode=trade_mode)
    ws_url = "wss://mockapi.kiwoom.com:10000/api/us/websocket"

    try:
        async with websockets.connect(ws_url, ping_interval=None) as websocket:
            await websocket.send(json.dumps({"trnm": "LOGIN", "token": token}))
            await websocket.recv()
            
            sub_data = {
                "trnm": "REG",
                "header": {
                    "api-id": "F5",
                    "Authorization": f"Bearer {token}"  # Capital A!
                },
                "body": {
                    "trnm": "REG",
                    "grp_no": "1",
                    "refresh": "1",
                    "data": None,
                    "- item": '[{"jmcode":"TQQQ","stex_tp":"ND"}]',
                    "- type": "F5"
                }
            }
            await websocket.send(json.dumps(sub_data))
            resp = await asyncio.wait_for(websocket.recv(), timeout=3)
            print("Response:", resp)
    except Exception as e:
        print("Error:", e)

asyncio.run(test_orig_capital_a())
