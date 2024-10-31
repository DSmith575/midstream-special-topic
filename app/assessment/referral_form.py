import time
from app.constants import PROCESSED_FOLDER
from app.documentProcessing import save_referral_form_to_pdf

def process_referral(ref_data):
    """Process the referral form data and save to PDF."""
    try:
        start_time = time.time()
        # Fix
        first_name = ref_data.get('personalInformation', {}).get('First Name', '')
        last_name = ref_data.get('personalInformation', {}).get('Last Name', '')
        pdf_path = save_referral_form_to_pdf(ref_data, first_name, last_name, PROCESSED_FOLDER)
        print(f"Processing time: {time.time() - start_time} seconds")
        return pdf_path
    except Exception as e:
        print(f"Error processing referral form: {e}")
        return None