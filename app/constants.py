import os
import sys

PROCESSED_DIR='processed'
UPLOADS_DIR='uploads'

CHUNK_LENGTH_MS = 120000  # 2 minutes
SILENCE_THRESHOLD = -30    # in dBFS
MIN_SILENCE_LEN = 1000     # in milliseconds

BASE_DIR = os.path.dirname(os.path.abspath(sys.executable)) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'processed')
ALLOWED_EXTENSIONS_AUDIO = {'wav', 'mp3', 'm4a', 'mp4'}
ALLOWED_EXTENSIONS_TEXT = {'pdf'}