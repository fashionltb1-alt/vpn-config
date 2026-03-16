import base64
import json
import socket
from urllib.parse import urlparse

INPUT_FILE = "nodes.txt"
OUTPUT_FILE = "servers.json"

servers = []

def check_server(host, port):
    try:
        socket.create_connection((host, int(port)), timeout=5)
        return True
    except:
        return False

with open(INPUT_FILE) as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()

    if line.startswith("vmess://"):
        encoded = line.replace("vmess://","")
        decoded = base64.b64decode(encoded + "==").decode()
        data = json.loads(decoded)

        host = data.get("add")
        port = int(data.get("port"))

        if check_server(host, port):
            servers.append({
                "name": data.get("ps","VMESS"),
                "type":"vmess",
                "address":host,
                "port":port,
                "uuid":data.get("id")
            })

result = {"servers":servers}

with open(OUTPUT_FILE,"w") as f:
    json.dump(result,f,indent=2)
