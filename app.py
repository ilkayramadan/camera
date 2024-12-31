from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": "https://your-netlify-domain"}})

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    if 'photo' in data:
        # Handle the photo (e.g., save or process)
        return jsonify({"message": "Photo uploaded successfully!"})
    else:
        return jsonify({"message": "No photo provided"}), 400
