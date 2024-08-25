from docx import Document

# Load the assessment form
assessment_doc = Document('./ReferralFormFilled.docx')

def extract_assessment_data(doc):
    data = {}
    section_found = False

    for paragraph in doc.paragraphs:
        if "Section 1: Personal Information" in paragraph.text:
            section_found = True

        if section_found and "Name (First & Last)" in paragraph.text:
            data['name'] = paragraph.text.split(":")[1].strip()
        if "Title" in paragraph.text:
            data['title'] = paragraph.text.split(":")[1].strip()
        if "Preferred Name" in paragraph.text:
            data['preferred_name'] = paragraph.text.split(":")[1].strip()
        if "Address" in paragraph.text:
            data['address'] = paragraph.text.split(":")[1].strip()
        if "Contact" in paragraph.text:
            data['contact'] = paragraph.text.split(":")[1].strip()
        if "Email" in paragraph.text:
            data['email'] = paragraph.text.split(":")[1].strip()
        if "Preferred Contact" in paragraph.text:
            data['preferred_contact'] = paragraph.text.split(":")[1].strip()
        if "Date of Birth" in paragraph.text:
            data['dob'] = paragraph.text.split(":")[1].strip()
        if "Gender" in paragraph.text:
            data['gender'] = paragraph.text.split(":")[1].strip()
        if "Pronoun" in paragraph.text:
            data['pronoun'] = paragraph.text.split(":")[1].strip()
        if "Residency Status" in paragraph.text:
            data['residency_status'] = paragraph.text.split(":")[1].strip()
        if "Ethnicity" in paragraph.text:
            data['ethnicity'] = paragraph.text.split(":")[1].strip()
        if "Iwi" in paragraph.text:
            data['iwi'] = paragraph.text.split(":")[1].strip()
        if "First Language" in paragraph.text:
            data['first_language'] = paragraph.text.split(":")[1].strip()
        if "Interpreter" in paragraph.text:
            data['interpreter'] = paragraph.text.split(":")[1].strip()
        if "Cultural Support" in paragraph.text:
            data['cultural_support'] = paragraph.text.split(":")[1].strip()
        if "Communication Needs" in paragraph.text:
            data['communication_needs'] = paragraph.text.split(":")[1].strip()
    return data

assessment_data = extract_assessment_data(assessment_doc)
print(assessment_data)
