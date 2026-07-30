import asyncio
import websockets
import json
import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from core.cavr import get_access_token

async def test_flat_int():
    # Test KR (0B) - Flat with integers and no hyphens
    print("\n--- Test KR (0B) - Flat with integers, no hyphens ---")
    try:
        token_kr = get_access_token("KR", force=True, trade_mode="MOCK")
        ws_url_kr = "wss://mockapi.kiwoom.com:10000/api/dostk/websocket"
        async with websockets.connect(ws_url_kr, ping_interval=None) as websocket:
            await websocket.send(json.dumps({"trnm": "LOGIN", "token": token_kr}))
            await websocket.recv()
            
            sub_kr = {
                "trnm": "REG",
                "grp_no": 1,
                "refresh": 1,
                "data": "",
                "item": "005930",
                "type": "0B"
            }
            await websocket.send(json.dumps(sub_kr))
            print("Response:", await websocket.recv())
    except Exception as e:
        print("Error KR:", e)

asyncio.run(test_flat_int())
