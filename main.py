from flask import Flask, render_template, request, redirect, send_file, jsonify
import subprocess
import os
import sys
from audio_processing import process_audio
import logging
import re
import traceback

app = Flask(__name__)

logging.basicConfig(level=logging.ERROR, filename='flask_errors.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def handle_exception(e):
    logging.error(f"An error occurred: {str(e)}")
    logging.error(traceback.format_exc())
    return jsonify({"error": str(e)}), 500

BASE_DIR = os.path.dirname(os.path.abspath(sys.executable)) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'processed')
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'mp4'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

def is_ffmpeg_installed():
    try:
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


def allowed_file(filename):
    if not filename:
        return False
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def sanitize_filename(filename):
    name = os.path.splitext(filename)[0]
    name = re.sub(r'[^a-zA-Z0-9_\-]', '_', name)  # Replace non-alphanumeric with underscores
    return name


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    logging.info("Upload route called.")

    if 'file' not in request.files:
        logging.error("No file part in the request")
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        logging.error("No file selected")
        return redirect(request.url)

    if not allowed_file(file.filename):
        logging.error("Invalid file uploaded")
        return redirect(request.url)

    filename = sanitize_filename(file.filename) + '.' + file.filename.rsplit('.', 1)[1].lower()
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        file.save(filepath)
        logging.info(f"File saved to {filepath}")
    except Exception as e:
        logging.error(f"Failed to save file: {e}")
        return "Failed to save file", 500

    try:
        processed_document, processed_result = process_audio(filepath)
        logging.info(f"Audio processed: {processed_document}")
    except Exception as e:
        logging.error(f"Audio processing failed: {e}")
        return "An error occurred during audio processing", 500

    # Ensure processed_document is a string
    if not isinstance(processed_document, str) or not os.path.exists(processed_document):
        logging.error("Processed file not found or is not a valid path")
        return "Processed file not found", 404

    try:
        return send_file(processed_document, as_attachment=True, download_name=os.path.basename(processed_document))
    except Exception as e:
        logging.error(f"Error sending file: {e}")
        return "Error sending file", 500


def run_flask_app():
    app.run(port=5000, debug=True, use_reloader=False)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
    if not os.access(UPLOAD_FOLDER, os.W_OK):
        raise PermissionError(f"Cannot write to upload folder: {UPLOAD_FOLDER}")
    if not os.access(PROCESSED_FOLDER, os.W_OK):
        raise PermissionError(f"Cannot write to processed folder: {PROCESSED_FOLDER}")
    run_flask_app()