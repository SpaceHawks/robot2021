# Communication related functions
import asyncio
import websockets
import threading
import pickle

class Tether:
    def __init__(self, handler, host="0.0.0.0", port=8080):
        self.handler = handler

        start_server = websockets.serve(self.respond, host, port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    
    def respond(self, res, path):
        while True:
            msg = await res.recv()
            await self.realrespond(msg, path, res)
    
    def realrespond(self, msg, path, res):
        print(msg, path, res)

    def send(self, msg):
        pass #! TODO
    
