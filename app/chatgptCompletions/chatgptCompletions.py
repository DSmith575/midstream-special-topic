from openai import OpenAI
import os
from dotenv import load_dotenv
import re

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

def process_client_audio(audio_path):
    """Main processing function: chunk audio, process, transcribe, and convert."""
    try:
        # with open(audio_path, "rb") as audio_file:  # Automatically closes the file
        #     # Transcribe audio using OpenAI's Whisper model
        #     transcript = client.audio.transcriptions.create(
        #         model="whisper-1",
        #         file=audio_file,
        #     )
        print("Processing audio file:", audio_path)
        audio_file=open(audio_path, "rb")
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        audio_file.close()
        # cleaned_transcript = re.sub(r'[^\w\s,.?!;:()-]', '', transcript)
        # print("Transcript:", cleaned_transcript)

        # remove the audio file
        try:
            os.remove(audio_path)
        except Exception as e:
            print(f"Error removing audio file: {e}")
            raise

        return transcript
    
    except Exception as e:
        print(f"Failed to process audio: {e}")
        raise

def get_relevant_information(section, text):
    prompt = (f"Based on the following text, does the person mentioned have any issues related to {section}? do not include asking if there are any issues, just provide the information.\n\n"
              f"If yes, provide details. Text: {text} try to turn it into a usable narrative.\n\n"
              f"If there is nothing related to {section}, please just return No information found."
              )
    
    # prompt = (f"Based on the following transcribed audio text, does the person mentioned have any issues related to {section}? Provide a narrative of relevant information only.\n\n"
    #       f"Text: {text} \n\n"
    #       f"If there is nothing related to {section}, indicate that there are no issues related to {section}."
    #      )
    
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
        'Background, Present Living Situation, Significant Events, and Contingency Plan': [
            'A short narrative of the person\'s background', 'Current living situation etc',
        ],
        'Communication': [
            'Ability to express core needs Verbal or Non-Verbal', 'Can read/write?',
            'Can use a phone?',
            'Receptive / Expressive skills?'
        ],
        'Sensory and Speech difficulties': [
            'Blind or nearly blind', 'Deaf or nearly deaf', 'Hearing impaired', 'Speech impaired', 'Vision impaired',
        ],
        'Mobility': [
            'Driving', 'Falling or history of falling', 'Getting up after falling', 'Moving around in the community', 'Moving around inside home',
            'Moving Around Outside home', 'Transfers, wheelchair to car or bed to chair', 'Two or one assistance for all transfers',
            'Using arms, hands, or fingers', 'Using transport as a passenger', 'Wheelchair user',
        ],
        'Household Management': [
            'Faecal smearing', 'Administering personal finances', 'Garden / lawns', 
            'Home safety', 'Laundry', 'Operating home heating appliances', 
            'Meal preparation', 'Shopping for necessary items', 'Other housework'
        ],
        'Self-care': [
            'Bathing, showering, Washing self', 'Bed mobility', 'Dressing and / or undressing', 
            'Eating and drinking', 'Faecal smearing', 'Grooming and caring for body parts', 
            'Managing / preventing health problems', 'Managing medication', 
            'Menstrual management', 'Night Care', 'Night settling', 'Toileting'
        ],
        'Continence': [
            'Faecal continence', 'Urinary continence',
        ],
        # Add other sections accordingly
    }

    print("Sections:", sections)  

    for section, items in sections.items():
        if section not in form_data:
            form_data[section] = {}
        
        for item in items:
            print(f"Looking for item: {item}") 
            response = get_relevant_information(item, text)
            
            if response is None:
                print(f"Warning: No relevant information found for {item}")
            else:
                print(f"Found relevant information for {item}: {response}")

            form_data[section][item] = response  # Update the item-response pair
    print('FORM_DATA',form_data)


    return form_data