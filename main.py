from flask import Flask, request, redirect, url_for, send_from_directory, render_template, send_file
import os
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['PROCESSED_FOLDER'] = './processed'
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3', 'm4a', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def remove_filename_extension(file):
    filename, file_extension = os.path.splitext(file.filename)
    return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        split_filename = remove_filename_extension(file)
        filename = split_filename + '.' + file.filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            result = subprocess.run(['python', 'audio_processing.py', filepath], check=True, capture_output=True, text=True)
            print("STDOUT:")
            print(result.stdout)
            print("STDERR:")
            print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Error in audio_process.py: {e}")
            print("STDOUT:")
            print(e.stdout)
            print("STDERR:")
            print(e.stderr)
            return "An error occurred during audio processing", 500

        processed_document = os.path.join(app.config['PROCESSED_FOLDER'], f"{split_filename}-processed" + '.docx')

        if not os.path.exists(processed_document):
            return "Processed file not found", 404
        
        return send_file(processed_document, as_attachment=True)
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['PROCESSED_FOLDER']):
        os.makedirs(app.config['PROCESSED_FOLDER'])
    app.run(debug=True)