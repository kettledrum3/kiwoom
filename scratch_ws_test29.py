import asyncio
import websockets
import json
import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from core.cavr import get_access_token

async def test_delay():
    market = "US"
    trade_mode = "MOCK"
    token = get_access_token(market, force=True, trade_mode=trade_mode)
    ws_url = "wss://mockapi.kiwoom.com:10000/api/us/websocket"

    try:
        async with websockets.connect(ws_url, ping_interval=None) as websocket:
            await websocket.send(json.dumps({"trnm": "LOGIN", "token": token}))
            resp = await websocket.recv()
            print("Login response:", resp)
            
            # SLEEP for 1 second!
            print("Sleeping for 1 second...")
            await asyncio.sleep(1)
            
            sub_data = {
                "trnm": "REG",
                "header": {
                    "api-id": "FE",
                    "authorization": f"Bearer {token}"
                },
                "body": {
                    "trnm": "REG",
                    "grp_no": "1",
                    "refresh": "1",
                    "data": None,
                    "- item": "TQQQ",
                    "- type": "FE"
                }
            }
            await websocket.send(json.dumps(sub_data))
            resp2 = await asyncio.wait_for(websocket.recv(), timeout=3)
            print("Sub response:", resp2)
    except Exception as e:
        print("Error:", e)

asyncio.run(test_delay())
