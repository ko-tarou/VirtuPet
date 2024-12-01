import asyncio
import websockets
import os
import time

connected_clients = set()
IMAGE_DIR = "images"  # 画像を保存するディレクトリ

if not os.path.exists(IMAGE_DIR):
	os.makedirs(IMAGE_DIR)

async def handle_client(websocket):
	print("A client connected")
	connected_clients.add(websocket)
	try:
		async for message in websocket:
			if isinstance(message, bytes):
				print(f"Received binary data: {len(message)} bytes")
				timestamp = int(time.time() * 1000)
				file_path = os.path.join(IMAGE_DIR, f"image_{timestamp}.jpg")
				with open(file_path, "wb") as f:
					f.write(message)
				print(f"Image saved as {file_path}")
			else:
				print(f"Received text message: {message}")
	except websockets.exceptions.ConnectionClosed as e:
		print(f"Client disconnected: {e}")
	finally:
		connected_clients.remove(websocket)

async def main():
	print("Starting WebSocket server...")
	async with websockets.serve(handle_client, "0.0.0.0", 12345):
		print("WebSocket server running on ws://0.0.0.0:12345")
		await asyncio.Future()

if __name__ == "__main__":
	asyncio.run(main())