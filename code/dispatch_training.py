import urllib.request
import json
import time

GABRIEL_IP = "10.0.0.27"
PORT = "5000"

def send_command(endpoint, payload):
    """Send command to Gabriel"""
    url = f"http://{GABRIEL_IP}:{PORT}/{endpoint}"
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.load(response)
    except Exception as e:
        return {"status": "error", "message": str(e)}

def start_training():
    """Initiate training on Gabriel"""
    print("--- DISPATCH: Starting Angel Cloud Training ---")
    result = send_command("train", {
        "command": "start_training",
        "params": {"epochs": 1, "batch_size": 1}
    })
    print(f"Response: {result}")
    return result

def check_status():
    """Check training progress"""
    result = send_command("train", {"command": "check_status"})
    return result

def monitor_training(check_interval=30):
    """Monitor training until complete"""
    print("\n--- MONITORING TRAINING ---")
    while True:
        status = check_status()
        
        if status.get("status") == "success":
            training = status.get("training", {})
            progress = training.get("progress")
            running = training.get("running")
            
            print(f"[{time.strftime('%H:%M:%S')}] Status: {progress} | Running: {running}")
            
            if not running and progress in ["complete", "failed"]:
                print("\n--- TRAINING FINISHED ---")
                if training.get("last_result"):
                    print(f"Result: {training['last_result']}")
                break
        
        time.sleep(check_interval)

if __name__ == "__main__":
    # Start training
    start_training()
    
    # Monitor until complete
    time.sleep(5)  # Give it time to start
    monitor_training(check_interval=30)