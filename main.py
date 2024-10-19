from flask import Flask, render_template, request, redirect, send_file, jsonify
import subprocess
import os
import sys
from audio_processing import process_audio
from assessment_form import process_data
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# Base directories for file uploads and processing
BASE_DIR = os.path.dirname(os.path.abspath(sys.executable)) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'processed')
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'mp4', 'pdf'}

# Flask app configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
# app.config['ALLOWED_TEXT_EXTENSIONS'] = ALLOWED_TEXT_EXTENSIONS

# Utility functions
def is_ffmpeg_installed():
    """Check if FFmpeg is installed."""
    try:
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def allowed_file(filename):
    """Check if the file is allowed based on the extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def sanitize_filename(filename):
    """Sanitize the filename by removing or replacing invalid characters."""
    name = os.path.splitext(filename)[0]
    return re.sub(r'[^a-zA-Z0-9_\-]', '-', name)

def handle_exception(e):
    """Log and return an error message as JSON."""
    # logging.error(f"An error occurred: {str(e)}")
    # logging.error(traceback.format_exc())
    return jsonify({"error": str(e)}), 500

# Routes
@app.route('/')
def index():
    """Render the main index page."""
    return render_template('index.html')

@app.route('/referral-form')
def referral_form():
    """Render the referral form page."""
    return render_template('referral-form.html')

@app.route('/audio-processing')
def audio_processing():
    """Render the audio processing page."""
    return render_template('audio-processing.html')

@app.route('/assessment-form')
def assessment_form():
    """Render the audio processing page."""
    return render_template('assessment-form.html')

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    """Handle audio file upload and processing."""
    if 'file' not in request.files:
        # logging.error("No file part in the request.")
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        # logging.error("No file selected.")
        return redirect(request.url)

    if not allowed_file(file.filename):
        # logging.error("Invalid file extension.")
        return redirect(request.url)

    filename = sanitize_filename(file.filename) + '.' + file.filename.rsplit('.', 1)[1].lower()
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # logging.info(f"File uploaded: {filename}")

    # Save uploaded file
    try:
        file.save(filepath)
        # logging.info(f"File saved to {filepath}")
    except Exception as e:
        # logging.error(f"Failed to save file: {e}")
        return "Failed to save file", 500

    # Process the audio file
    try:
        processed_document = process_audio(filepath)
        # logging.info(f"Audio processed: {processed_document}")
    except Exception as e:
        # logging.error(f"Audio processing failed: {e}")
        return "An error occurred during audio processing", 500

    # Check if processed document is valid and exists
    if not isinstance(processed_document, str) or not os.path.exists(processed_document):
        # logging.error("Processed file not found or invalid.")
        return "Processed file not found", 404

    # Send processed file for download
    try:
        response = send_file(
            processed_document,
            as_attachment=True,
            download_name=os.path.basename(processed_document),
        )
        response.headers['Content-Disposition'] = f'attachment; filename="{os.path.basename(processed_document)}"'
        return response
    except Exception as e:
        # logging.error(f"Error sending file: {e}")
        return "Error sending file", 500
    
@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    
    print("OG FILE", file)
    if file.filename == '':
        return redirect(request.url)

    if not allowed_file(file.filename):
        return redirect(request.url)
    

    filename = sanitize_filename(file.filename) + '.' + file.filename.rsplit('.', 1)[1].lower()
    print("SANITIZED FILENAME", filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print("FILEPATH", filepath)

    try:
        file.save(filepath)
        print("FILE SAVED", filepath)
    except Exception as e:
        return "Failed to save PDF file", 500

    try:
        processed_document = process_data(filepath)

    except Exception as e:
        return "An error occured during processing", 500
    
    if not isinstance(processed_document, str) or not os.path.exists(processed_document):
        # logging.error("Processed file not found or invalid.")
        return "Processed file not found", 404

    try:
        response = send_file(
            processed_document,
            as_attachment=True,
            download_name=os.path.basename(processed_document),
        )
        response.headers['Content-Disposition'] = f'attachment; filename="{os.path.basename(processed_document)}"'
        return response
    except Exception as e:
        # logging.error(f"Error sending file: {e}")
        return "Error sending file", 500


def run_flask_app():
    """Run the Flask app."""
    # app.run(port=5000, debug=True, use_reloader=False)
    app.run()

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

    if not os.access(UPLOAD_FOLDER, os.W_OK):
        raise PermissionError(f"Cannot write to upload folder: {UPLOAD_FOLDER}")
    if not os.access(PROCESSED_FOLDER, os.W_OK):
        raise PermissionError(f"Cannot write to processed folder: {PROCESSED_FOLDER}")

    run_flask_app()