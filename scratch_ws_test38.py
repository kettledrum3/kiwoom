import asyncio
import websockets
import json
import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from core.cavr import get_access_token

async def run_tests():
    # 1. Test FE (US Realtime Prices)
    print("\n--- Test FE (US Realtime Prices) ---")
    try:
        token_us = get_access_token("US", force=True, trade_mode="MOCK")
        ws_url_us = "wss://mockapi.kiwoom.com:10000/api/us/websocket"
        async with websockets.connect(ws_url_us, ping_interval=None) as websocket:
            await websocket.send(json.dumps({"trnm": "LOGIN", "token": token_us}))
            print("Login response US:", await websocket.recv())
            
            items = [{"jmcode": "TQQQ", "stex_tp": "ND"}]
            payload_fe = {
                "trnm": "REG",
                "grp_no": "1",
                "refresh": "1",
                "data": [
                    {
                        "item": [json.dumps(items)],
                        "type": ["FE"]
                    }
                ]
            }
            send_data = json.dumps(payload_fe)
            print("Sending US payload:", send_data)
            await websocket.send(send_data)
            resp = await asyncio.wait_for(websocket.recv(), timeout=3)
            print("Response US FE:", resp)
    except Exception as e:
        print("Error FE:", e)

    # 2. Test 0B (KR Realtime Prices) - Variant A: just the ticker
    print("\n--- Test 0B (KR Realtime Prices) - Variant A: '005930' ---")
    try:
        token_kr = get_access_token("KR", force=True, trade_mode="MOCK")
        ws_url_kr = "wss://mockapi.kiwoom.com:10000/api/dostk/websocket"
        async with websockets.connect(ws_url_kr, ping_interval=None) as websocket:
            await websocket.send(json.dumps({"trnm": "LOGIN", "token": token_kr}))
            print("Login response KR:", await websocket.recv())
            
            payload_0b_a = {
                "trnm": "REG",
                "grp_no": "1",
                "refresh": "1",
                "data": [
                    {
                        "item": ["005930"],
                        "type": ["0B"]
                    }
                ]
            }
            send_data = json.dumps(payload_0b_a)
            print("Sending KR payload A:", send_data)
            await websocket.send(send_data)
            resp = await asyncio.wait_for(websocket.recv(), timeout=3)
            print("Response KR 0B (Variant A):", resp)
    except Exception as e:
        print("Error 0B A:", e)

    # 3. Test 0B (KR Realtime Prices) - Variant B: with 'KRX:' prefix
    print("\n--- Test 0B (KR Realtime Prices) - Variant B: 'KRX:005930' ---")
    try:
        token_kr = get_access_token("KR", force=True, trade_mode="MOCK")
        ws_url_kr = "wss://mockapi.kiwoom.com:10000/api/dostk/websocket"
        async with websockets.connect(ws_url_kr, ping_interval=None) as websocket:
            await websocket.send(json.dumps({"trnm": "LOGIN", "token": token_kr}))
            print("Login response KR:", await websocket.recv())
            
            payload_0b_b = {
                "trnm": "REG",
                "grp_no": "1",
                "refresh": "1",
                "data": [
                    {
                        "item": ["KRX:005930"],
                        "type": ["0B"]
                    }
                ]
            }
            send_data = json.dumps(payload_0b_b)
            print("Sending KR payload B:", send_data)
            await websocket.send(send_data)
            resp = await asyncio.wait_for(websocket.recv(), timeout=3)
            print("Response KR 0B (Variant B):", resp)
    except Exception as e:
        print("Error 0B B:", e)

asyncio.run(run_tests())
