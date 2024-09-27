from flask import Flask, request, redirect, send_file, render_template
import os
import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from threading import Thread
import time
import logging


from audio_processing import process_audio
# from form_validation import validate_document

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(sys.executable)) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'processed')
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'mp4'}

logging.basicConfig(
    filename=os.path.join(BASE_DIR, 'app.log'),  
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s'
)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_filename(filename):
    return os.path.splitext(filename)[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        app.logger.warning("No file part in the request")
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        app.logger.warning("Invalid file uploaded")
        return redirect(request.url)

    filename = sanitize_filename(file.filename) + '.' + file.filename.rsplit('.', 1)[1].lower().replace(" ", "-")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        file.save(filepath)
        app.logger.info(f"File saved to {filepath}")
    except Exception as e:
        app.logger.error(f"Failed to save file: {e}")
        return "Failed to save file", 500

    try:
        processed_document = process_audio(filepath)
        app.logger.info(f"Audio processed: {processed_document}")
    except Exception as e:
        app.logger.error(f"Audio processing failed: {e}")
        return "An error occurred during audio processing", 500

    if not os.path.exists(processed_document):
        app.logger.error("Processed file not found")
        return "Processed file not found", 404

    try:
        return send_file(processed_document, as_attachment=True, download_name=os.path.basename(processed_document))
    except Exception as e:
        app.logger.error(f"Error sending file: {e}")
        return "Error sending file", 500

@app.route('/upload-document', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.docx'):
        return redirect(request.url)
    
    filename = sanitize_filename(file.filename) + '.docx'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    if not process_document_file(filepath):
        return "An error occurred during document processing", 500
    
    processed_document = os.path.join(app.config['PROCESSED_FOLDER'], f"{sanitize_filename(filename)}-processed.docx")
    if not os.path.exists(processed_document):
        return "Processed file not found", 404
    
    return send_file(processed_document, as_attachment=True)

def process_document_file(filepath):
    try:
        result = subprocess.run(['python', 'form_validation.py', filepath], check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        return False

def run_flask():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
    app.run(port=5000, debug=False)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My Flask App GUI")

        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        self.browser.setUrl(QUrl('http://127.0.0.1:5000/'))

if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    time.sleep(2) 

    # Start the PyQt application
    qt_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(qt_app.exec_())