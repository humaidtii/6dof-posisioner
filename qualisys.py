import asyncio
import qtm
import colorama
import time
import sys
import time

import xml.etree.cElementTree as ET
from threading import Thread

labels = []

class QtmChecker(Thread):
    def __init__(self):
        Thread.__init__(self)
    
        self.bodies = []
        self.pos = {}
        self.connection = None
        self._stay_open = True

        self.start()

    def run(self):
        asyncio.run(self._async_run())

    def close(self):
        self._stay_open = False
        self.join()

    async def _async_run(self):
        await self._connect()
        while(self._stay_open):
            await asyncio.sleep(1)
        await self._close()

    async def update_bodies(self):
        params = await self.connection.get_parameters(parameters=["6d"])
        xml = ET.fromstring(params)
        self.bodies = [label.text for label in xml.iter('Name')]

    async def _connect(self):
        """ Main function """
        self.connection = await qtm.connect(host="192.168.0.2", version="1.20", timeout=5)
        if self.connection is None:
            print("Connection failed")
            return

        await self.update_bodies()

        await self.connection.stream_frames(
            components=['6D'],
            on_packet=self._on_packet)

    def _on_packet(self, packet):
        header, bodies = packet.get_6d()
        if bodies is not None:
            for rigid in self.bodies:
                index = self.bodies.index(rigid)
                body = bodies[index]
                x = round(body[0][0] / 1000, 3)
                y = round(body[0][1] / 1000, 3)
                z = round(body[0][2] / 1000, 3)
                self.pos[rigid] = [x, y, z]
