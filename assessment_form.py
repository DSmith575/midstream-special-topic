import openai
import fitz
import os


openai.api_key = 'sk-zyhGEaHsxDg2nQhmmI-WI_ffRJ3IQNgCE8pkw_1BSAT3BlbkFJQq_PNWDk7SfFsyZ9U1O8YNTp3qfDyP75jCMd5Zh2wA'

def extract_text_from_pdf(filepath):
    """Extract text from a PDF file.

    Args:
        filepath (str): Path to the PDF file.

    Returns:
        str: Extracted text or None if the file doesn't exist or an error occurs.
    """
    if not os.path.isfile(filepath):
        print(f"File does not exist: {filepath}")
        return None

    try:
        # Open the PDF file
        doc = fitz.open(filepath)
        text = ""
        
        # Extract text from each page
        for page in doc:
            text += page.get_text("text")  # Extract text as plain text

        return text

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None


def get_relevant_information(section, text):
    prompt = f"Based on the following text, does the person mentioned have any issues related to {section}? If yes, provide details. Text: {text}"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150
        # API_KEY=API_KEY
    )
    return response.choices[0].text.strip()


def analyze_pdf_for_form(text):
    form_data = {}

    sections = {
        'Household Management': [
            'Faecal smearing', 'Administering personal finances', 'Garden / lawns', 
            'Home safety', 'Laundry', 'Operating home heating appliances', 
            'Meal preparation', 'Shopping for necessary items', 'Other housework'
        ],
        'Self-care': [
            'Bathing, showering, washing self', 'Bed mobility', 'Dressing and / or undressing', 
            'Eating and drinking', 'Faecal smearing', 'Grooming and caring for body parts', 
            'Managing / preventing health problems', 'Managing medication', 
            'Menstrual management', 'Night Care', 'Night settling', 'Toileting'
        ],
        # Add other sections accordingly
    }

    for section, items in sections.items():
        for item in items:
            response = get_relevant_information(item, text)
            form_data[item] = response

    return form_data