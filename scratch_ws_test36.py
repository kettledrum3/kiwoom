import asyncio
import websockets
import json
import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from core.cavr import get_access_token

async def test_no_type_field():
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
                    "api-id": "FE",
                    "authorization": f"Bearer {token}"
                },
                "body": {
                    "trnm": "REG",
                    "grp_no": "1",
                    "refresh": "1",
                    "data": [
                        {
                            "item": ["TQQQ"]  # List of strings, no type!
                        }
                    ]
                }
            }
            await websocket.send(json.dumps(sub_data))
            resp = await asyncio.wait_for(websocket.recv(), timeout=3)
            print("Response:", resp)
    except Exception as e:
        print("Error:", e)

asyncio.run(test_no_type_field())
