import asyncio
import websockets
import json
import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from core.cavr import get_access_token

async def run_tests():
    # 1. Test 00 (KR Execution)
    print("\n--- Test 00 (KR Execution) ---")
    try:
        token_kr = get_access_token("KR", force=True, trade_mode="MOCK")
        ws_url_kr = "wss://mockapi.kiwoom.com:10000/api/dostk/websocket"
        async with websockets.connect(ws_url_kr, ping_interval=None) as websocket:
            await websocket.send(json.dumps({"trnm": "LOGIN", "token": token_kr}))
            print("Login response KR:", await websocket.recv())
            
            payload_00 = {
                "trnm": "REG",
                "grp_no": "1",
                "refresh": "1",
                "data": [
                    {
                        "item": [""],
                        "type": ["00"]
                    }
                ]
            }
            send_data = json.dumps(payload_00)
            print("Sending KR payload 00:", send_data)
            await websocket.send(send_data)
            resp = await asyncio.wait_for(websocket.recv(), timeout=3)
            print("Response KR 00:", resp)
    except Exception as e:
        print("Error 00:", e)

asyncio.run(run_tests())
