import asyncio
import qtm
import colorama
import time
import sys
import time

import xml.etree.cElementTree as ET

labels = []

def fetch_labels():
    #asyncio.ensure_future(setup())
    #asyncio.get_event_loop().run_until_complete()
    return asyncio.run(setup())

async def setup():
    global labels
    """ Main function """
    connection = await qtm.connect(host="192.168.0.2", version="1.20", timeout=5)
    if connection is None:
        print("Connection failed")
        return
    
    params = await connection.get_parameters(parameters=["6d"])
    xml = ET.fromstring(params)
    labels = [label.text for label in xml.iter('Name')]
    print(labels)
    return labels


