import asyncio
import websockets
import json
import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from core.cavr import get_access_token

async def run_tests():
    market = "US"
    trade_mode = "MOCK"
    token = get_access_token(market, force=True, trade_mode=trade_mode)
    ws_url = "wss://mockapi.kiwoom.com:10000/api/us/websocket"

    # Test Case 1: Flat structure as described in the guide
    print("\n--- Test Case 1: Flat, item & type as lists of strings ---")
    try:
        async with websockets.connect(ws_url, ping_interval=None) as websocket:
            # Login
            await websocket.send(json.dumps({"trnm": "LOGIN", "token": token}))
            login_resp = await websocket.recv()
            print("Login response:", login_resp)
            
            items = [{"jmcode": "TQQQ", "stex_tp": "ND"}]
            payload = {
                "trnm": "REG",
                "grp_no": "1",
                "refresh": "1",
                "data": [
                    {
                        "item": [json.dumps(items)],
                        "type": ["F5"]
                    }
                ]
            }
            send_data = json.dumps(payload)
            print("Sending payload:", send_data)
            await websocket.send(send_data)
            resp = await asyncio.wait_for(websocket.recv(), timeout=3)
            print("Response:", resp)
    except Exception as e:
        print("Error in Test Case 1:", e)

    # Test Case 2: Nested structure (header/body) but with correct arrays inside data
    print("\n--- Test Case 2: Header/Body nested, item & type as lists of strings ---")
    try:
        async with websockets.connect(ws_url, ping_interval=None) as websocket:
            # Login
            await websocket.send(json.dumps({"trnm": "LOGIN", "token": token}))
            login_resp = await websocket.recv()
            print("Login response:", login_resp)
            
            items = [{"jmcode": "TQQQ", "stex_tp": "ND"}]
            payload = {
                "trnm": "REG",
                "header": {
                    "api-id": "F5",
                    "authorization": f"Bearer {token}"
                },
                "body": {
                    "trnm": "REG",
                    "grp_no": "1",
                    "refresh": "1",
                    "data": [
                        {
                            "item": [json.dumps(items)],
                            "type": ["F5"]
                        }
                    ]
                }
            }
            send_data = json.dumps(payload)
            print("Sending payload:", send_data)
            await websocket.send(send_data)
            resp = await asyncio.wait_for(websocket.recv(), timeout=3)
            print("Response:", resp)
    except Exception as e:
        print("Error in Test Case 2:", e)

asyncio.run(run_tests())
