
from app.documentProcessing import save_form_data_to_pdf, extract_text_from_pdf
from app.chatgptCompletions import analyze_completions_for_form
import time


def process_data(pdf_path, filename, process_path):
    try:
        start_time = time.time()
        extracted_text = extract_text_from_pdf(pdf_path)
        form_data = analyze_completions_for_form(extracted_text)
        save_doc = save_form_data_to_pdf(form_data, filename, process_path)

        print(f"Processed data saved as PDF: {pdf_path}")

        print(f"Processing time: {time.time() - start_time:.2f} seconds")

        return save_doc
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        raise


