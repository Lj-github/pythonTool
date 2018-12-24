# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 下午4:16
import asyncio
import websockets

import asyncio
import websockets  # https://websockets.readthedocs.io/en/stable/
import base64
import json
import os
from _flask.lib import lzstring

x = lzstring.LZString()


async def echo(websocket, path):
    async for message in websocket:
        # 接受到的消息
        msg = json.loads(message)
        msgID = int(msg['id'])
        # {id: 1, idx: 0, txt: allMsg[0]}
        if msgID == 1:
            txt = msg['txt']
            #comStr = x.decompress(txt)
            with open('img/' + str(msg['idx']) + '', 'w') as f:
                f.write(txt)
            rsp = {}
            rsp["id"] = 2
            rsp["res"] = 1
            await websocket.send(json.dumps(rsp))
        elif msgID == 111:
            os.system("python3 img2Video2.py")
            await websocket.send("publish success!!!")


asyncio.get_event_loop().run_until_complete(websockets.serve(echo, '192.168.1.214', 9999))
asyncio.get_event_loop().run_forever()
print("begin")
