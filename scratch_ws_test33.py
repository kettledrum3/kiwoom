import asyncio
import websockets
import json
import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from core.cavr import get_access_token

async def test_compact_json():
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
                    "authorization": f"Bearer {token}"
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
            # Serialize with separators=(',', ':') to strip all whitespace!
            compact_payload = json.dumps(sub_data, separators=(',', ':'))
            print("Sending compact payload:", compact_payload)
            await websocket.send(compact_payload)
            resp = await asyncio.wait_for(websocket.recv(), timeout=3)
            print("Response:", resp)
    except Exception as e:
        print("Error:", e)

asyncio.run(test_compact_json())
