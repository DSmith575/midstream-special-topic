from flask import Flask, render_template, request, redirect, send_file
import os
from app.assessment.audio_processing import process_audio
from app.assessment.assessment_form import process_data
from app.assessment.referral_form import process_referral
from app.constants import UPLOAD_FOLDER, PROCESSED_FOLDER, ALLOWED_EXTENSIONS_AUDIO, ALLOWED_EXTENSIONS_TEXT
from app.fileUploads.file_uploads import allowed_file, sanitize_filename, handle_exception

app = Flask(__name__)

# Flask app configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['ALLOWED_EXTENSIONS_AUDIO'] = ALLOWED_EXTENSIONS_AUDIO
app.config['ALLOWED_EXTENSIONS_TEXT'] = ALLOWED_EXTENSIONS_TEXT


# create folder
def create_folders():
    """Create the necessary folders for file uploads and processed files."""
    for folder in [UPLOAD_FOLDER, PROCESSED_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)

# Routes
@app.route('/')
def index():
    """Render the main index page."""
    create_folders()
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
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        print("NO FILE")
        return redirect(request.url)

    if not allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS_AUDIO']):
        print("NOT ALLOWED")
        return redirect(request.url)

    filename = sanitize_filename(file.filename) + '.' + file.filename.rsplit('.', 1)[1].lower()
    print("FILENAME", filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print("FILEPATH", filepath)

    # Save uploaded file
    try:
        file.save(filepath)
        print("FILE SAVED", filepath)
    except Exception as e:
        print(f"Failed to save file: {e}")  # Log the error
        return "Failed to save file", 500

    # Process the audio file
    try:
        processed_document = process_audio(filepath)
    except Exception as e:
        return "An error occurred during audio processing", 500

    # Check if processed document is valid and exists
    if not isinstance(processed_document, str) or not os.path.exists(processed_document):
        return "Processed file not found", 404
    
    # remove files from uploads
    try:
        os.remove(filepath)
    except Exception as e:
        return "Error removing file", 500
    
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
        return "Error sending file", 500
    
@app.route('/upload-referral-form', methods=['POST'])
def upload_referral_form():
    """Handle referral form upload and processing."""

    try:
        ref_data = request.get_json()
        if ref_data is None:
            return "No data received", 400
        print("REF DATA", ref_data)

        processed_document = process_referral(ref_data)

    except Exception as e:
        return "An error occurred during processing", 500
    
    if not isinstance(processed_document, str) or not os.path.exists(processed_document):
        return "Processed file not found", 404
    
    try:
        response = send_file(
            processed_document,
            as_attachment=True,
            download_name=os.path.basename(processed_document),
        )
        response.headers['Content-Disposition'] = f'attachment; filename="{os.path.basename(processed_document)}'
        return response
    except Exception as e:
        return "Error sending file", 500
    
    
@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    
    print("OG FILE", file)
    if file.filename == '':
        return redirect(request.url)

    if not allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS_TEXT']):
        return redirect(request.url)
    

    filename = sanitize_filename(file.filename) + '.' + file.filename.rsplit('.', 1)[1].lower()
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        file.save(filepath)
        print("FILE SAVED", filepath)
    except Exception as e:
        return "Failed to save PDF file", 500

    try:
        processed_document = process_data(filepath, filename, app.config['PROCESSED_FOLDER'])

    except Exception as e:
        return "An error occurred during processing", 500
    
    if not isinstance(processed_document, str) or not os.path.exists(processed_document):
        return "Processed file not found", 404
    

    try:
        os.remove(filepath)
    except Exception as e:
        return "Error removing file", 500
    
    try:
        response = send_file(
            processed_document,
            as_attachment=True,
            download_name=os.path.basename(processed_document),
        )
        response.headers['Content-Disposition'] = f'attachment; filename="{os.path.basename(processed_document)}"'
        
        return response
    except Exception as e:
        return "Error sending file", 500


def run_flask_app():
    """Run the Flask app."""
    app.run(port=5000, host='0.0.0.0', debug=True)

if __name__ == '__main__':
    run_flask_app()