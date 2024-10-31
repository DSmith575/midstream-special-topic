import os
import sys

PROCESSED_DIR='processed'
UPLOADS_DIR='uploads'

CHUNK_LENGTH_MS = 120000  # 2 minutes
SILENCE_THRESHOLD = -30    # in dBFS
MIN_SILENCE_LEN = 1000     # in milliseconds

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'static', 'processed')
ALLOWED_EXTENSIONS_AUDIO = {'wav', 'mp3', 'm4a', 'mp4'}
ALLOWED_EXTENSIONS_TEXT = {'pdf'}

GPT_COMPLETION_SECTIONS = {
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
        'Behaviour': [
            'Harm to others, Mood and emotion (anxiety, depression, unstable mood. etc)', 'Motivation',
            'Property damage', 'Repetitive', 'Routine', 'Self-harming',
            'Sleep and night behaviour (insomnia, excessive sleep, etc)', 'Socially inappropriate,',
            'Unsafe wandering', 'Withdrawn'
        ],
        'Memory / Cognition' : [
            'Attention', 'Intellectual ability',
            'Memory', 'Orientation', 'Learning ability / Problem solving',
        ],
        'Supervision' : [
            'Daily prompts', 'Needs 24-hour supervision', 'Some, for safety',
        ],
        'Recreational and Social': [
            'Community participation', 'Educational support', 'Specialist Teachers',
            'Family life', ' Socialization', 'Vocational support',
        ], 
            
        # Add other sections accordingly
    }