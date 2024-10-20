
from app.documentProcessing import save_form_data_to_pdf, extract_text_from_pdf
from app.chatgptCompletions import analyze_completions_for_form
import time
from app.constants import PROCESSED_DIR, UPLOADS_DIR
import os

def create_directories():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(UPLOADS_DIR, exist_ok=True)

def process_data(pdf_path):
    try:
        create_directories()
        start_time = time.time()
        extracted_text = extract_text_from_pdf(pdf_path)
        form_data = analyze_completions_for_form(extracted_text)
        save_doc = save_form_data_to_pdf(form_data, PROCESSED_DIR)

        print(f"Processed data saved as PDF: {pdf_path}")

        print(f"Processing time: {time.time() - start_time:.2f} seconds")

        return save_doc
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        raise


