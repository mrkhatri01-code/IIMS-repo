import os
from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
from werkzeug.utils import secure_filename
import shutil
import glob

# Import the pipeline main function
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run_pipeline import main as run_pipeline_main

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# --- Config ---
INPUT_DIR = os.path.join(os.path.dirname(__file__), '../input')
CLIPS_DIR = os.path.join(os.path.dirname(__file__), '../output/clips')
CAPTIONS_DIR = os.path.join(os.path.dirname(__file__), '../output/captions')

# --- Serve Frontend ---
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)

# --- Upload Video ---
@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return 'No file part', 400
    file = request.files['video']
    if file.filename == '':
        return 'No selected file', 400
    filename = secure_filename('match.mp4')
    save_path = os.path.join(INPUT_DIR, filename)
    os.makedirs(INPUT_DIR, exist_ok=True)
    file.save(save_path)
    return 'OK', 200

# --- Run Highlight Pipeline ---
@app.route('/run', methods=['POST'])
def run_pipeline():
    # Clean previous outputs
    if os.path.exists(CLIPS_DIR):
        shutil.rmtree(CLIPS_DIR)
    if os.path.exists(CAPTIONS_DIR):
        shutil.rmtree(CAPTIONS_DIR)
    os.makedirs(CLIPS_DIR, exist_ok=True)
    os.makedirs(CAPTIONS_DIR, exist_ok=True)
    # Run the pipeline
    run_pipeline_main()
    return 'OK', 200

# --- Get Results ---
@app.route('/results', methods=['GET'])
def results():
    # Find all clips and captions
    clips = sorted(glob.glob(os.path.join(CLIPS_DIR, 'clip_*.mp4')))
    results = []
    for clip_path in clips:
        base = os.path.splitext(os.path.basename(clip_path))[0]
        caption_path = os.path.join(CAPTIONS_DIR, base.replace('clip_', 'clip_') + '.txt')
        # Read caption
        caption = ''
        if os.path.exists(caption_path):
            with open(caption_path, 'r') as f:
                caption = f.read().strip()
        # Serve video via /clips/ endpoint
        results.append({
            'clip_url': f'/clips/{os.path.basename(clip_path)}',
            'caption': caption
        })
    return jsonify(results)

# --- Serve Clips ---
@app.route('/clips/<filename>')
def serve_clip(filename):
    return send_from_directory(CLIPS_DIR, filename)

# --- Main ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 