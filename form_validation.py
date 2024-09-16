from docx import Document
from docx.shared import Pt
from datetime import datetime


# config = {
#     "sections": {
#         "personal_info": "Section 1: Personal Information",
#         "medical_info": "Section 2: Medical Information"
#     },
#     "labels": {
#         "title": "Title (Mr/Mrs/Ms/etc.):",
#     }
# }

# # Use the configuration dictionary in your function calls
# client_details = {
#     'Title:': extract_text(
#         input_doc,
#         config["labels"]["title"],
#         config["sections"]["personal_info"],
#         config["sections"]["medical_info"]
#     ),
# }

# Load the input and output documents
input_doc = Document('ReferralFormFilled.docx')
output_doc = Document('OutputFormEmpty.docx')

# Function to extract text from paragraphs based on a keyword
def extract_text(doc, keyword, start_text=None, end_text=None):
    start_found = False if start_text else True
    for para in doc.paragraphs:
        # Check for starting text point
        if start_text and start_text in para.text:
            start_found = True
            continue

        # Check for ending text point
        if end_text and end_text in para.text:
            start_found = False
            continue

        # If within the desired range, extracts data
        if start_found and keyword in para.text:
            return para.text.split(keyword)[1].strip()
  

def fill_fields(output_doc, data, start_text=None, end_text=None):
    start_found = False if start_text else True
    for paragraph in output_doc.paragraphs:

        if start_text and start_text in paragraph.text:
            print("found start text")
            start_found = True
            continue

        # Check for end marker
        if end_text and end_text in paragraph.text:
            print("end Text")
            start_found = False
            continue

        # If within range, starts replacing text
        if start_found:
            print('here')
            for key, value in data.items():
                if key in paragraph.text:
                    print(f"Replacing '{key}' with '{value}'")
                    for run in paragraph.runs:
                        if key in run.text:
                            print(f"Replacing '{key}' with '{value}'")
                            run.text = run.text.replace(key, f"{key} {value}")

def split_name(name):
    name_parts = name.split(' ')
    return name_parts[0], ' '.join(name_parts[1:])

def split_disabilities(disabilities):
    return disabilities.split(',')




def insert_bullet_points(output_doc, data, start_text=None, end_text=None):
    start_found = False if start_text else True

    styles = output_doc.styles
    print(styles)

    for style in styles:
        print(style.name)
    for paragraph in output_doc.paragraphs:

        if start_text and start_text in paragraph.text:
            start_found = True
            continue

        if end_text and end_text in paragraph.text:
            start_found = False
            continue 

        if start_found:
            for key, value in data.items():
                if key in paragraph.text:
                    paragraph.clear()
                    items = value.split(', ')
                    for item in items:
                        new_run = paragraph.add_run(f"•  {item.strip()}")
                        font = new_run.font
                        font.name = 'Times New Roman'
                        font.size = Pt(12)
                        font.bold = True
                        new_run.add_break()


assessment_details = {
    'The assessment was completed on:': datetime.now().strftime("%d/%m/%Y"),
    'Name:': extract_text(input_doc, "Name (First & Last):"),
    'NHI:': extract_text(input_doc, "National Health Index (NHI) Number:"),
}

client_details = {
    'Last name:': split_name(extract_text(input_doc, "Name (First & Last):", "Section 1: Personal Information", "Section 2: Medical Information"))[1],
    'First name:': split_name(extract_text(input_doc, "Name (First & Last):", "Section 1: Personal Information", "Section 2: Medical Information"))[0],
    'NHI number:' : extract_text(input_doc, "National Health Index (NHI) Number:", "Section 1: Personal Information", "Section 2: Medical Information"),
    'Title:': extract_text(input_doc, "Title (Mr/Mrs/Ms/etc.):", "Section 1: Personal Information", "Section 2: Medical Information"),
    'Marital status:': extract_text(input_doc, "Marital Status:", "Section 1: Personal Information", "Section 2: Medical Information") or "Single",
    'Address:': extract_text(input_doc, "Address:", "Section 1: Personal Information", "Section 2: Medical Information"),
    'Mobile:': extract_text(input_doc, "Contact Number:", "Section 1: Personal Information", "Section 2: Medical Information"),
    'Email:': extract_text(input_doc, "Email:", "Section 1: Personal Information", "Section 2: Medical Information"),
    'Date of birth:': extract_text(input_doc, "Date of Birth:", "Section 1: Personal Information", "Section 2: Medical Information"),
    'Gender:': extract_text(input_doc, "Gender:", "Section 1: Personal Information", "Section 2: Medical Information"),
    'Ethnicity:': extract_text(input_doc, "Ethnicity:", "Section 1: Personal Information", "Section 2: Medical Information"),
    'Iwi / Hapū (if Māori):' : extract_text(input_doc, "Iwi / Hapū (if Māori):", "Section 1: Personal Information", "Section 2: Medical Information"),
    'First language:': extract_text(input_doc, "First Language (if not English):", "Section 1: Personal Information", "Section 2: Medical Information"),
    'Interpreter required:': extract_text(input_doc, "Interpreter Required:", "Section 1: Personal Information", "Section 2: Medical Information"),
    'Cultural support required:': extract_text(input_doc, "Cultural Support Required:", "Section 1: Personal Information", "Section 2: Medical Information"),
    "Communication needs:": extract_text(input_doc, "Communication Needs:", "Section 1: Personal Information", "Section 2: Medical Information"),
    "Preferred contact method:": extract_text(input_doc, "Preferred Contact Method:", "Section 1: Personal Information", "Section 2: Medical Information"),
    "Name of GP:": extract_text(input_doc, "Doctor/GP Name:", "Section 2: Medical Information", "Section 3: Disability Information"),
    "GP’s phone number:": extract_text(input_doc, "Medical Centre Contact Number:", "Section 2: Medical Information", "Section 3: Disability Information"),
    "Primary disability:": split_disabilities(extract_text(input_doc, "Disability Name/Type:", "Section 3: Disability Information", "Section 4: Additional Information"))[0],
    "Interim eligibility:": extract_text(input_doc, "Interim Eligibility:", "Section 1: Personal Information", "Section 2: Medical Information") or "No",
}

alt_contact = {
    'Last name:': split_name(extract_text(input_doc, "Name (First & Last):", "Section 5: Alternative Contact (Optional)", "Section 6: Referrer’s Contact Details"))[1],
    'First name': split_name(extract_text(input_doc, "Name (First & Last):", "Section 5: Alternative Contact (Optional)", "Section 6: Referrer’s Contact Details"))[0],
    'Address:': extract_text(input_doc, "Address:", "Section 5: Alternative Contact (Optional)", "Section 6: Referrer’s Contact Details") or "N/A",
    'Home phone:': extract_text(input_doc, "Contact Number:", "Section 5: Alternative Contact (Optional)", "Section 6: Referrer’s Contact Details") or "N/A",
    'Mobile:': extract_text(input_doc, "Contact Number:", "Section 5: Alternative Contact (Optional)", "Section 6: Referrer’s Contact Details") or "N/A",
    'Email:': extract_text(input_doc, "Email:", "Section 5: Alternative Contact (Optional)", "Section 6: Referrer’s Contact Details") or "N/A",
    'Relationship to client:': extract_text(input_doc, "Relationship to the Person Referred:", "Section 5: Alternative Contact (Optional)", "Section 6: Referrer’s Contact Details") or "N/A",
    'Date of birth:': extract_text(input_doc, "Date of Birth:", "Section 5: Alternative Contact (Optional)", "Section 6: Referrer’s Contact Details") or "N/A",
}

disability_diagnosis = {
    '[Details]': extract_text(input_doc, "Disability Name/Type:", "Section 3: Disability Information", "Section 4: Additional Information"),
}



# Fill the output document with all required data
fill_fields(output_doc, assessment_details, "Assessment Information", "Client Details")
fill_fields(output_doc, client_details, "Client Details", "Disability / Diagnosis Details")
fill_fields(output_doc, alt_contact, "Alternative Contact Details", "Emergency Contact Details")
insert_bullet_points(output_doc, disability_diagnosis, "Disability / Diagnosis Details", "Reason for Assessment / Referral to Taikura Trust")




date_created = datetime.now().strftime("%d-%m-%Y")
output_doc.save(f"{date_created}_OutputForm.docx")
print("Data has been transferred and appended successfully.")