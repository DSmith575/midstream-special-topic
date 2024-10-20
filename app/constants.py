import os
import sys

PROCESSED_DIR='processed'
UPLOADS_DIR='uploads'

# CHUNK_LENGTH_MS = 120000  # 2 minutes
CHUNK_LENGTH_MS = 10000  # 10 seconds
SILENCE_THRESHOLD = -30    # in dBFS
MIN_SILENCE_LEN = 1000     # in milliseconds

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'static', 'processed')
ALLOWED_EXTENSIONS_AUDIO = {'wav', 'mp3', 'm4a', 'mp4'}
ALLOWED_EXTENSIONS_TEXT = {'pdf'}