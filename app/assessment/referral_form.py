import os
import sys
import time
from app.constants import PROCESSED_FOLDER, ALLOWED_EXTENSIONS_TEXT, ALLOWED_EXTENSIONS_AUDIO, UPLOAD_FOLDER
from app.documentProcessing import save_referral_form_to_pdf

def process_referral(ref_data):
    """Process the referral form data and save to PDF."""
    try:
        start_time = time.time()
        # Fix
        first_name = ref_data.get('section1', {}).get('firstname', '')
        print(f"Processing referral form for: {first_name}")
        last_name = ref_data.get('section1', {}).get('lastname', '')
        pdf_path = save_referral_form_to_pdf(ref_data, first_name, last_name, PROCESSED_FOLDER)
        print(f"Processing time: {time.time() - start_time} seconds")
        return pdf_path
    except Exception as e:
        print(f"Error processing referral form: {e}")
        return None