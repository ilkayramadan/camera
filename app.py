from flask import Flask, request, jsonify, send_from_directory
import base64
import os
import time

app = Flask(__name__)

# Directory to save photos
SAVE_DIR = os.path.join(os.getcwd(), "photos")
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_photo():
    try:
        data = request.json.get("photo")
        if not data:
            return jsonify({"error": "No photo data received"}), 400

        # Decode the base64 image data
        photo_data = data.split(",")[1]  # Remove "data:image/png;base64,"
        photo_bytes = base64.b64decode(photo_data)
        file_name = f"photo-{int(time.time())}.png"

        # Save the photo
        with open(os.path.join(SAVE_DIR, file_name), "wb") as f:
            f.write(photo_bytes)

        return jsonify({"message": f"Photo saved as {file_name}"}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to process photo"}), 500

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')  # Serve the HTML file

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
