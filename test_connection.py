#!/usr/bin/env python3
"""
Simple test script to verify the chatbot server is working
"""
import requests
import asyncio
import websockets
import json

def test_http_endpoint():
    """Test the HTTP endpoint"""
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ HTTP endpoint is working!")
            return True
        else:
            print(f"❌ HTTP endpoint returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ HTTP endpoint error: {e}")
        return False

async def test_websocket():
    """Test the WebSocket endpoint"""
    try:
        # Test RAG WebSocket
        uri = "ws://localhost:8000/ws/rag"
        async with websockets.connect(uri) as websocket:
            # Send a test message
            test_message = {
                "type": "message",
                "content": "Hello, this is a test",
                "session_id": "test_session"
            }
            await websocket.send(json.dumps(test_message))
            
            # Wait for response
            response = await websocket.recv()
            data = json.loads(response)
            
            if data.get("type") in ["thinking", "message", "error"]:
                print("✅ WebSocket connection is working!")
                return True
            else:
                print(f"❌ Unexpected WebSocket response: {data}")
                return False
                
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        return False

async def main():
    print("🧪 Testing AI Chatbot Server...")
    print("-" * 40)
    
    # Test HTTP
    http_ok = test_http_endpoint()
    
    # Test WebSocket
    websocket_ok = await test_websocket()
    
    print("-" * 40)
    if http_ok and websocket_ok:
        print("🎉 All tests passed! The server is ready to use.")
        print("📱 Open your browser and go to: http://localhost:8000")
    else:
        print("❌ Some tests failed. Please check the server logs.")

if __name__ == "__main__":
    asyncio.run(main())
