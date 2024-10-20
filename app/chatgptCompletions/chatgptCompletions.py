from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

def get_relevant_information(section, text):
    prompt = (f"Based on the following text, does the person mentioned have any issues related to {section}? "
              f"If yes, provide details. Text: {text}")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error getting response from OpenAI: {e}")
        return None
    

def analyze_completions_for_form(text):
    form_data = {}

    print("Analyzing PDF for form data...")
    sections = {
        'Household Management': [
            'Faecal smearing', 'Administering personal finances', 'Garden / lawns', 
            # 'Home safety', 'Laundry', 'Operating home heating appliances', 
            # 'Meal preparation', 'Shopping for necessary items', 'Other housework'
        ],
        'Self-care': [
            'Bathing, showering, washing self', 'Bed mobility', 'Dressing and / or undressing', 
            # 'Eating and drinking', 'Faecal smearing', 'Grooming and caring for body parts', 
            # 'Managing / preventing health problems', 'Managing medication', 
            # 'Menstrual management', 'Night Care', 'Night settling', 'Toileting'
        ],
        # Add other sections accordingly
    }

    print("Sections:", sections)  

    for section, items in sections.items():
        print(f"Analyzing section: {section}")
        for item in items:
            print(f"Looking for item: {item}") 
            response = get_relevant_information(item, text)
            
            if response is None:
                print(f"Warning: No relevant information found for {item}")
            else:
                print(f"Found relevant information for {item}: {response}")
            
            form_data[item] = response


    return form_data