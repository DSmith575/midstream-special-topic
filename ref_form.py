from docx import Document

# Load the assessment form
assessment_doc = Document('./ReferralFormFilled.docx')

def extract_assessment_data(doc):
    data = {}
    section_one = False

    for paragraph in doc.paragraphs:
        if "Section 1: Personal Information" in paragraph.text:
            section_one = True

        if section_one and "Name (First & Last)" in paragraph.text:
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
# print(assessment_data)

def concatFirstLastName(data):
    return data['name'].split(" ")[0] + " " + data['name'].split(" ")[1]

	# Load the referral form template
referral_doc = Document('OutputFormEmpty.docx')

def fill_referral_form(referral_doc, data):
    client_details = False

    in_section = False
    section_text = []

    for paragraph in referral_doc.paragraphs:
        if "Client Details" in paragraph.text:
            in_section = True

        if "Disability / Diagnosis Details" in paragraph.text:
            in_section = False

        if in_section:
            section_text.append(paragraph.text.strip())
            print(paragraph.text.strip())

    # for paragraph in referral_doc.paragraphs:
    #     for runs in paragraph.runs:
    #         if runs.bold and "Last name" in runs.text:
    #             runs.text += data['name'].split(" ")[1]
        # if "Last name" in paragraph.text:
        #     client_details = True
        # if client_details and "Last name" in paragraph.text:
        #     # Get Last name from paragraph.text
        #     start_idx = paragraph.text.findFirst("Last name")
        #     print(start_idx)
        #     # append name to the paragraph
            
        #     # paragraph.text = paragraph.text[:start_idx] + " " + data['name'] + paragraph.text[start_idx:]
            
        #     client_details = False
    
    # Save the filled referral form
    referral_doc.save('OutputFormEmptyTest.docx')

# Fill out the referral form with the extracted data
fill_referral_form(referral_doc, assessment_data)
    