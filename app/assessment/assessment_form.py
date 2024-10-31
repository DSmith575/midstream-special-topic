
from app.documentProcessing import save_form_data_to_pdf, extract_text_from_pdf, build_assessment_form, extract_referral_form_data_from_pdf
from app.chatgptCompletions import analyze_completions_for_form
import time


def process_data(audio_pdf_path, audio_filename,referral_form_pdf_path, referral_form_filename, process_path):
    try:
        start_time = time.time()
        extracted_text = extract_text_from_pdf(audio_pdf_path)
        audio_form_data = analyze_completions_for_form(extracted_text)
        # Narrative form builder
        save_audio_completions = save_form_data_to_pdf(audio_form_data, audio_filename, process_path)

        print(audio_form_data)
        ref_data = extract_referral_form_data_from_pdf(referral_form_pdf_path)

        assessment_form = build_assessment_form(
            audio_data=audio_form_data,
            referral_data=ref_data,
            process_path=process_path,
            filename=referral_form_filename)

        print(f"Processing time: {time.time() - start_time:.2f} seconds")
        return assessment_form
        # return save_audio_completions
    
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        raise