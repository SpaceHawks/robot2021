# Communication related functions
import websockets
import socket


class Tether:
    def __init__(self, handler, loop, host="0.0.0.0", port=8080):
        self.handler = handler
        self.host = host
        self.port = port

        start_server = websockets.serve(self.respond, host, port)
        loop.run_until_complete(start_server)

    
    async def respond(self, res, path):
        self.res = res
        async for msg in res:
            await self.realrespond(msg, path, res)
    
    async def realrespond(self, msg, path, res):
        # print(f"Got command: {msg}")
        self.handler(msg, self)

    async def send(self, msg):
        try:
            await self.res.send(msg)
            return True
        except Exception as e:
            # print("Cannot send message as no client is connected")
            return False
    
    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return f"{s.getsockname()[0]}:{self.port}"
