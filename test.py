import websocket
from time import sleep
ws=websocket.WebSocket()
ws.connect('ws://localhost:8000/ws/attend',header={'token':"d59ef4c7e556d7fb8ce84e355737d130424bede4"})
ws.send('hello world')


sleep(4)