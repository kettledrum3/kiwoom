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

    # Test Case 1: Literal Excel format (flat, with hyphens, data: "")
    print("\n--- Test Case 1: Flat with hyphens (Literal Excel) ---")
    try:
        async with websockets.connect(ws_url, ping_interval=None) as websocket:
            await websocket.send(json.dumps({"trnm": "LOGIN", "token": token}))
            print("Login:", await websocket.recv())
            
            payload = {
                "trnm": "REG",
                "grp_no": "1",
                "refresh": "1",
                "data": "",
                "- item": '[{"jmcode":"TQQQ","stex_tp":"ND"}]',
                "- type": "F5"
            }
            send_data = json.dumps(payload)
            print("Sending:", send_data)
            await websocket.send(send_data)
            resp = await asyncio.wait_for(websocket.recv(), timeout=3)
            print("Response:", resp)
    except Exception as e:
        print("Error:", e)

    # Test Case 2: Clean flat format (no hyphens, item & type lists inside data array)
    print("\n--- Test Case 2: Clean flat array (Guide format) ---")
    try:
        async with websockets.connect(ws_url, ping_interval=None) as websocket:
            await websocket.send(json.dumps({"trnm": "LOGIN", "token": token}))
            print("Login:", await websocket.recv())
            
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
            print("Sending:", send_data)
            await websocket.send(send_data)
            resp = await asyncio.wait_for(websocket.recv(), timeout=3)
            print("Response:", resp)
    except Exception as e:
        print("Error:", e)

asyncio.run(run_tests())
