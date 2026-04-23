import urllib.request
import json

# TARGET: Gabriel's Ethernet IP
GABRIEL_IP = "10.0.0.27"
PORT = "5000"
URL = f"http://{GABRIEL_IP}:{PORT}/process"

print(f"--- DISPATCHER LINK ---")
print(f"Targeting Gabriel at: {GABRIEL_IP}")

# The Message
payload = {
    "instruction": "Protocol 1: Initiate Handshake. Do you copy?"
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(URL, data=data, headers={'Content-Type': 'application/json'})

try:
    print("Sending packet...")
    with urllib.request.urlopen(req, timeout=5) as response:
        result = json.load(response)
        
    print("\n[SUCCESS] Response received from Gabriel:")
    print(f" >> {result['reply']}")
    print("\nCluster Link is VERIFIED.")

except Exception as e:
    print(f"\n[FAILURE] Link broken. Error: {e}")