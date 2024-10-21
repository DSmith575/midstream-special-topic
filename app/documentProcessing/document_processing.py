from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os
import pymupdf


def save_audio_transcription_to_pdf(transcription, filename, uploads_dir):
    pdf_filename = f"{filename}.pdf"
    pdf_filepath = os.path.join(uploads_dir, pdf_filename)
    try:
        doc = SimpleDocTemplate(pdf_filepath, pagesize=A4)
        story = []

        styles = getSampleStyleSheet()
        heading_style = ParagraphStyle(
            'ColoredHeading',
            parent=styles['Heading2'],
            textColor=colors.blue  # Set your desired color here
        )
        paragraph_style = styles['BodyText']

        if isinstance(transcription, dict) and 'text' in transcription:
            transcription_text = transcription['text']  # Get the main transcription text
        else:
            transcription_text = str(transcription)  # Fallback in case it's not as expected

        # Add title
        story.append(Paragraph('Audio Transcription', styles['Title']))
        story.append(Spacer(1, 12))  # Add space after title

        

        # Add transcription text
        story.append(Paragraph(transcription_text, paragraph_style))
        story.append(Spacer(1, 10))  # Add space after transcription

        # Build the PDF
        doc.build(story)
        return pdf_filepath
    except Exception as e:
        print(f"Failed to write transcription to PDF: {e}")
        return None


def save_form_data_to_pdf(form_data, filename, uploads_dir):
    output_filepath = os.path.join(uploads_dir, filename)

    try:
        # Create a PDF document
        doc = SimpleDocTemplate(output_filepath, pagesize=A4)
        story = []

        styles = getSampleStyleSheet()
        heading_style = ParagraphStyle(
            'ColoredHeading',
            parent=styles['Heading2'],
            textColor=colors.blue  # Set your desired color here
        )
        paragraph_style = styles['BodyText']

        # Add title
        story.append(Paragraph('Processed AI Transcription', styles['Title']))
        story.append(Spacer(1, 12))  # Add space after title

        # Write each key-value pair in form_data to the document
        for item, response in form_data.items():
            # Add heading
            story.append(Paragraph(item, heading_style))
            # Add paragraph
            story.append(Paragraph(str(response) if response else "No relevant information found.", paragraph_style))
            story.append(Spacer(1, 10))  # Add space after each item

        # Build the PDF
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
            # Extract text from each page
            for page in doc:
                text += page.get_text("text")

            return text

    except Exception as e:
        print(f"Error extracting text from PDF: {e} - File: {filepath}")
        return None
    

def save_referral_form_to_pdf(form_data, first_name, last_name, uploads_dir):
    pdf_filename = f"{first_name}-{last_name}.pdf"
    pdf_filepath = os.path.join(uploads_dir, pdf_filename)

    try:
        doc = SimpleDocTemplate(pdf_filepath, pagesize=A4)
        story = []

        styles = getSampleStyleSheet()
        heading_style = ParagraphStyle(
            'ColoredHeading',
            parent=styles['Heading2'],
            textColor=colors.blue
        )
        paragraph_style = styles['BodyText']

        # Add title
        story.append(Paragraph(f'{first_name} {last_name} Referral Form' , styles['Title']))
        story.append(Spacer(1, 12))  # Add space after title

        # Iterate through each section in the data object
        for section_key, section_value in form_data.items():
            # Add the section header
            story.append(Paragraph(section_value['header'], heading_style))
            story.append(Spacer(1, 6))  # Space after header
            
            # Add the content of the section
            for field, value in section_value.items():
                if field != 'header':  # Skip the header field
                    story.append(Paragraph(f"{field.replace('_', ' ').title()}: {value}", paragraph_style))
            
            story.append(Spacer(1, 12))  # Space after each section

        # Build the PDF
        doc.build(story)
        return pdf_filepath
    except Exception as e:
        print(f"An error occurred while creating the PDF: {e}")
