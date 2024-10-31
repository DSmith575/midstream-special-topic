from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os
import pymupdf


def save_audio_transcription_to_pdf(transcription, filename, uploads_dir):
    pdf_filename = f"{filename}-audio-transcription.pdf"
    pdf_filepath = os.path.join(uploads_dir, pdf_filename)
    try:
        doc = SimpleDocTemplate(pdf_filepath, pagesize=A4)
        story = []

        styles = getSampleStyleSheet()

        paragraph_style = styles['BodyText']

        if isinstance(transcription, dict) and 'text' in transcription:
            transcription_text = transcription['text']
        else:
            transcription_text = str(transcription)


        story.append(Paragraph(f'{pdf_filename} Audio Transcription', styles['Title']))
        story.append(Spacer(1, 12))

        

        # Add transcription text
        story.append(Paragraph(transcription_text, paragraph_style))
        story.append(Spacer(1, 10))

        doc.build(story)
        return pdf_filepath
    except Exception as e:
        print(f"Failed to write transcription to PDF: {e}")
        return None


def save_form_data_to_pdf(form_data, filename, uploads_dir):
    output_filepath = os.path.join(uploads_dir, filename)

    try:
        doc = SimpleDocTemplate(output_filepath, pagesize=A4)
        story = []

        styles = getSampleStyleSheet()
        heading_style = ParagraphStyle(
            'ColoredHeading',
            parent=styles['Heading2'],
            textColor=colors.blue
        )

        subheading_style = ParagraphStyle(
            'ColoredSubheading',
            parent=styles['Heading3'],
            textColor=colors.black
        )

        paragraph_style = styles['BodyText']


        story.append(Paragraph('Processed AI Transcription', styles['Title']))
        story.append(Spacer(1, 12))
 
        for section, items in form_data.items():

            story.append(Paragraph(section, heading_style))
            story.append(Spacer(1, 6))

            for item, response in items.items():
                # Add item as the subheading
                story.append(Paragraph(item, subheading_style))
                
                # Add the response as a paragraph
                story.append(Paragraph(str(response) if response else "No relevant information found.", paragraph_style))
                
                story.append(Spacer(1, 6))

        doc.build(story)
        return output_filepath
    
    except Exception as e:
        print(f"Failed to write processed data: {e}")
        return None
    
def extract_text_from_pdf(filepath):
    if not os.path.isfile(filepath):
        print(f"File does not exist: {filepath}")
        return None

    try:
        with pymupdf.open(filepath) as doc:
            text = ""
            for page in doc:
                text += page.get_text("text")

            return text

    except Exception as e:
        print(f"Error extracting text from PDF: {e} - File: {filepath}")
        return None
    

def save_referral_form_to_pdf(form_data, first_name, last_name, processed_dir):
    pdf_filename = f"{first_name}-{last_name}-referral-form.pdf"
    print(f"Saving referral form to PDF: {pdf_filename}")
    pdf_filepath = os.path.join(processed_dir, pdf_filename)

    try:
        doc = SimpleDocTemplate(pdf_filepath, pagesize=A4)
        story = []

        styles = getSampleStyleSheet()
        heading_style = ParagraphStyle(
            'ColoredHeading',
            parent=styles['Heading2'],
            textColor=colors.black
        )
        paragraph_style = styles['BodyText']

        # Add title
        story.append(Paragraph(f'{first_name} {last_name} Referral Form', styles['Title']))
        story.append(Spacer(1, 12))

        # Iterate through each section in the data object
        for section_key, section_value in form_data.items():
            # Add the section header
            story.append(Paragraph(section_value['header'], heading_style))

            story.append(Spacer(1, 6))
            
            # Add the content of the section
            for field, value in section_value.items():
                  # Skip the header field
                if field != 'header':
                    # Create a combined paragraph for the field name and value
                    combined_paragraph = Paragraph(
                        f"<b>{field.replace('_', ' ').title() if field != 'NHI' else 'NHI'}:</b> {value}",
                        paragraph_style
                    )
                    story.append(combined_paragraph)

                    
            
            story.append(Spacer(1, 12))

        doc.build(story)

        return pdf_filepath
    except Exception as e:
        print(f"An error occurred while creating the PDF: {e}")
