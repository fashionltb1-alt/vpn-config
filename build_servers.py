import base64
import json
import socket
import requests

INPUT_FILE = "nodes.txt"
OUTPUT_FILE = "servers.json"

servers = []

def check_server(host, port):
    try:
        socket.create_connection((host, int(port)), timeout=5)
        return True
    except:
        return False

def get_country(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = r.json()
        return data.get("country","Unknown"), data.get("countryCode","XX")
    except:
        return "Unknown","XX"

with open(INPUT_FILE) as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()

    if line.startswith("vmess://"):

        try:
            encoded = line.replace("vmess://","")
            decoded = base64.b64decode(encoded + "==").decode()
            data = json.loads(decoded)

            host = data.get("add")
            port = int(data.get("port"))

            if check_server(host, port):

                country, code = get_country(host)

                servers.append({
                    "name": data.get("ps","VMESS"),
                    "type": "vmess",
                    "country": country,
                    "countryCode": code,
                    "address": host,
                    "port": port,
                    "uuid": data.get("id")
                })

        except:
            continue

result = {"servers": servers}

with open(OUTPUT_FILE,"w") as f:
    json.dump(result,f,indent=2)
