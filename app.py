from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # To handle Cross-Origin Resource Sharing (CORS)
import base64
import os
import time

app = Flask(__name__)

# Allow requests from the specific frontend domain (e.g., Netlify)
CORS(app, origins=["https://your-netlify-app.netlify.app"])  # Update with your actual frontend URL

# Directory to save photos
SAVE_DIR = os.path.join(os.getcwd(), "photos")
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_photo():
    try:
        # Get photo data from the incoming request
        data = request.json.get("photo")
        if not data:
            return jsonify({"error": "No photo data received"}), 400  # Return error if no photo data is found

        # Decode the base64 image data (remove the "data:image/png;base64," part)
        photo_data = data.split(",")[1]
        photo_bytes = base64.b64decode(photo_data)
        
        # Create a unique file name using the current timestamp
        file_name = f"photo-{int(time.time())}.png"
        
        # Save the photo to the disk
        with open(os.path.join(SAVE_DIR, file_name), "wb") as f:
            f.write(photo_bytes)

        # Return success response with the file name
        return jsonify({"message": f"Photo saved as {file_name}"}), 200

    except Exception as e:
        # Catch any error and return a failure message
        print(e)
        return jsonify({"error": "Failed to process photo"}), 500

@app.route('/')
def serve_index():
    # Serve the HTML file when the root endpoint is accessed
    return send_from_directory('.', 'index.html')  # Ensure index.html is in the same directory as this script

if __name__ == '__main__':
    # Run the Flask app, make it publicly available on all network interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)
