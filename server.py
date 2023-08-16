# 服务端

import asyncio
import threading
import websockets

class WSServer:

    def __init__(self, port):
        self.server = websockets.serve(self.handler, "", port)
        self.connected = set()
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.server)
        self.thread = threading.Thread(target=self.loop.run_forever)
        self.thread.start()
        print("LOG: WS启动成功")

    async def handler(self, websocket):
        self.connected.add(websocket)
        print("LOG: A client has connected.")
        try:
            async for msg in websocket:
                print(f"< {msg}")
                # await websocket.send(msg)
        except websockets.exceptions.ConnectionClosedError:
            print("LOG: connection closed error")
        print("LOG: A client has lefted.")
        self.connected.remove(websocket)

    def send(self, content):
        # websockets.broadcast(self.connected, content)
        for connection in self.connected:
            if connection.open :
                asyncio.run(connection.send(content))

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
        print("LOG: WS服务已关闭")

if __name__ == "__main__":
    ws = WSServer(8765)
    while True:
        # print(len(ws.connected))
        try:
            x = input()
            ws.send(x)
        except (EOFError, KeyboardInterrupt):
            ws.stop()
            break