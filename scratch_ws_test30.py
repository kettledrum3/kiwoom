import asyncio
import websockets
import json
import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from core.cavr import get_access_token

async def test_header_token():
    market = "US"
    trade_mode = "MOCK"
    token = get_access_token(market, force=True, trade_mode=trade_mode)
    ws_url = "wss://mockapi.kiwoom.com:10000/api/us/websocket"

    # Try 1: token instead of authorization in header
    print("\n--- Try 1: token in header ---")
    try:
        async with websockets.connect(ws_url, ping_interval=None) as websocket:
            await websocket.send(json.dumps({"trnm": "LOGIN", "token": token}))
            await websocket.recv()
            
            sub_data = {
                "trnm": "REG",
                "header": {
                    "api-id": "FE",
                    "token": token
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
            resp = await asyncio.wait_for(websocket.recv(), timeout=3)
            print("Response:", resp)
    except Exception as e:
        print("Error:", e)

    # Try 2: token with Bearer prefix in header
    print("\n--- Try 2: token with Bearer prefix in header ---")
    try:
        async with websockets.connect(ws_url, ping_interval=None) as websocket:
            await websocket.send(json.dumps({"trnm": "LOGIN", "token": token}))
            await websocket.recv()
            
            sub_data = {
                "trnm": "REG",
                "header": {
                    "api-id": "FE",
                    "token": f"Bearer {token}"
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
            resp = await asyncio.wait_for(websocket.recv(), timeout=3)
            print("Response:", resp)
    except Exception as e:
        print("Error:", e)

asyncio.run(test_header_token())
