import os
import re
from flask import jsonify

def allowed_file(filename, app_config):
    """Check if the file is allowed based on the extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app_config

def sanitize_filename(filename):
    """Sanitize the filename by removing or replacing invalid characters."""
    name = os.path.splitext(filename)[0]
    return re.sub(r'[^a-zA-Z0-9_\-]', '-', name)

def handle_exception(e):
    """Log and return an error message as JSON."""
    # logging.error(f"An error occurred: {str(e)}")
    # logging.error(traceback.format_exc())
    return jsonify({"error": str(e)}), 500