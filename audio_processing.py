import os
import sys
import numpy as np
from pydub import AudioSegment
from pydub.silence import detect_silence
from pydub.utils import make_chunks
import noisereduce as nr
import whisper
from docx import Document
import torch
import time
import logging
import pythoncom
from docx2pdf import convert



logging.basicConfig(level=logging.ERROR, filename='error.log', filemode='a', 
                    format='%(asctime)s - %(levelname)s - %(message)s')


CHUNK_LENGTH_MS = 120000  # 2 minutes
SILENCE_THRESHOLD = -30    # in dBFS
MIN_SILENCE_LEN = 1000     # in milliseconds
PROCESSED_DIR = 'processed'
UPLOADS_DIR = 'uploads'

# --- Utility Functions ---
def create_directories():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(UPLOADS_DIR, exist_ok=True)

def clean_existing_files(filename):
    """Remove existing processed files."""
    for filename in os.listdir(PROCESSED_DIR):
            file_path = os.path.join(PROCESSED_DIR, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logging.info(f"Removed file: {file_path}")
            except Exception as e:
                logging.error(f"Failed to remove {file_path}: {e}")

def process_chunk(chunk):
    """Reduce noise and trim silence from an audio chunk."""
    reduced_chunk = nr.reduce_noise(y=np.array(chunk.get_array_of_samples()), 
                                    sr=chunk.frame_rate, prop_decrease=0.8)
    audio = AudioSegment(reduced_chunk.tobytes(), frame_rate=chunk.frame_rate, 
                         sample_width=chunk.sample_width, channels=chunk.channels)

    # Trim silence
    silences = detect_silence(audio, min_silence_len=MIN_SILENCE_LEN, 
                              silence_thresh=SILENCE_THRESHOLD)
    return audio[silences[0][0]:silences[-1][1]] if silences else audio

def transcribe_audio(model, audio_path):
    """Use Whisper model to transcribe audio."""
    return model.transcribe(audio_path, language="en", verbose=True)

def save_transcription(transcription, filename, processed=True):
    """Save transcription as a DOCX file."""
    docx_filename = f"{filename}-{'processed' if processed else 'original'}.docx"
    docx_path = os.path.join(PROCESSED_DIR, docx_filename)

    doc = Document()
    doc.add_heading(f"Transcription: {filename}", level=1)
    doc.add_paragraph(transcription["text"])
    doc.save(docx_path)
    return docx_path

def convert_to_pdf(docx_path):
    """Convert DOCX to PDF."""
    try:
        pythoncom.CoInitialize()
        pdf_path = docx_path.replace(".docx", ".pdf")
        convert(docx_path, pdf_path)
        return pdf_path
    except Exception as e:
        logging.error(f"Error converting {docx_path} to PDF: {str(e)}")
        raise
    finally:
        pythoncom.CoUninitialize()

def process_audio(audio_path):
    """Main processing function: chunk audio, process, transcribe, and convert."""
    try:
        start_time = time.time()
        create_directories()

        # Load audio and clean previous files
        audio = AudioSegment.from_file(audio_path)
        filename = os.path.splitext(os.path.basename(audio_path))[0]
        clean_existing_files(filename)

        # Process and combine chunks
        processed_audio = sum([process_chunk(chunk) for chunk in make_chunks(audio, CHUNK_LENGTH_MS)])
        processed_wav_path = os.path.join(PROCESSED_DIR, f"{filename}.wav")
        processed_audio.export(processed_wav_path, format="wav")

        # Load Whisper model and transcribe
        model = whisper.load_model("large", device="cuda" if torch.cuda.is_available() else "cpu")
        transcription = transcribe_audio(model, processed_wav_path)

        # Save transcription and convert to PDF
        docx_path = save_transcription(transcription, filename)
        pdf_path = convert_to_pdf(docx_path)

        print(f"Processed transcription saved as PDF: {pdf_path}")
        print(f"Processing time: {time.time() - start_time:.2f} seconds")

        return pdf_path
    except Exception as e:
        logging.error(f"Error processing audio: {str(e)}")
        raise

# --- Entry Point ---
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python audio_process.py <audio_path>")
        sys.exit(1)
    process_audio(sys.argv[1])