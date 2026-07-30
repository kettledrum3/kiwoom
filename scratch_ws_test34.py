import asyncio
import websockets
import json
import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from core.cavr import get_access_token

async def test_correct_nested_items():
    # 1. Test KR (0B) - item with "KRX:" prefix inside data list
    print("\n--- Test KR (0B) - item with 'KRX:' prefix inside data list ---")
    try:
        token_kr = get_access_token("KR", force=True, trade_mode="MOCK")
        ws_url_kr = "wss://mockapi.kiwoom.com:10000/api/dostk/websocket"
        async with websockets.connect(ws_url_kr, ping_interval=None) as websocket:
            await websocket.send(json.dumps({"trnm": "LOGIN", "token": token_kr}))
            await websocket.recv()
            
            sub_kr = {
                "trnm": "REG",
                "header": {
                    "api-id": "0B",
                    "authorization": f"Bearer {token_kr}"
                },
                "body": {
                    "trnm": "REG",
                    "grp_no": "1",
                    "refresh": "1",
                    "data": [
                        {
                            "item": "KRX:005930",  # "KRX:" prefix!
                            "type": "0B"
                        }
                    ]
                }
            }
            await websocket.send(json.dumps(sub_kr))
            print("Response:", await websocket.recv())
    except Exception as e:
        print("Error KR:", e)

    # 2. Test US (FE) - item as Map structure inside data list
    print("\n--- Test US (FE) - item as Map structure inside data list ---")
    try:
        token_us = get_access_token("US", force=True, trade_mode="MOCK")
        ws_url_us = "wss://mockapi.kiwoom.com:10000/api/us/websocket"
        async with websockets.connect(ws_url_us, ping_interval=None) as websocket:
            await websocket.send(json.dumps({"trnm": "LOGIN", "token": token_us}))
            await websocket.recv()
            
            sub_us = {
                "trnm": "REG",
                "header": {
                    "api-id": "FE",
                    "authorization": f"Bearer {token_us}"
                },
                "body": {
                    "trnm": "REG",
                    "grp_no": "1",
                    "refresh": "1",
                    "data": [
                        {
                            "item": [{"jmcode": "TQQQ", "stex_tp": "ND"}],
                            "type": "FE"
                        }
                    ]
                }
            }
            await websocket.send(json.dumps(sub_us))
            print("Response:", await websocket.recv())
    except Exception as e:
        print("Error US:", e)

asyncio.run(test_correct_nested_items())
