import base64
import json
import socket
import requests

INPUT_FILE = "nodes.txt"
OUTPUT_FILE = "servers.json"

servers = []


# ✅ Fix base64 padding
def decode_base64(data):
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    return base64.b64decode(data).decode("utf-8")


# ✅ Check if server is reachable
def check_server(host, port):
    try:
        socket.create_connection((host, int(port)), timeout=3)
        return True
    except:
        return False


# ✅ Get country info
def get_country(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = r.json()
        return data.get("country", "Unknown"), data.get("countryCode", "XX")
    except:
        return "Unknown", "XX"


# ✅ Read file
with open(INPUT_FILE) as f:
    lines = f.readlines()


for line in lines:
    line = line.strip()

    if not line.startswith("vmess://"):
        continue

    try:
        encoded = line[8:]
        decoded = decode_base64(encoded)
        data = json.loads(decoded)

        host = data.get("add")
        port = int(data.get("port", 0))

        if not host or not port:
            continue

        # 🚨 Check server alive
        if not check_server(host, port):
            continue

        country, code = get_country(host)

        server = {
            "name": data.get("ps", "VMESS"),
            "type": "vmess",
            "country": country,
            "countryCode": code,
            "address": host,
            "port": port,
            "uuid": data.get("id"),

            # 🔥 NEW FIELDS
            "network": data.get("net", "tcp"),
            "path": data.get("path", ""),
            "host": data.get("host", ""),
            "tls": data.get("tls", ""),
            "sni": data.get("sni", ""),
            "alpn": data.get("alpn", ""),
        }

        servers.append(server)

    except Exception as e:
        print("Error parsing line:", e)
        continue


# ✅ Save result
result = {"servers": servers}

with open(OUTPUT_FILE, "w") as f:
    json.dump(result, f, indent=2)

print(f"✅ Saved {len(servers)} working servers to {OUTPUT_FILE}")
