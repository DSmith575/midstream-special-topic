import os
import sys
from pydub import AudioSegment
from pydub.utils import make_chunks
import whisper
import torch
import time
from app.constants import PROCESSED_DIR, CHUNK_LENGTH_MS, SILENCE_THRESHOLD, MIN_SILENCE_LEN
from app.audioHelpers import process_chunks, transcribe_audio
from app.documentProcessing import save_audio_transcription_to_pdf

def process_audio(audio_path):
    """Main processing function: chunk audio, process, transcribe, and convert."""
    try:
        start_time = time.time()
        # Load audio and clean previous files
        audio = AudioSegment.from_file(audio_path)
        filename = os.path.splitext(os.path.basename(audio_path))[0]
        # Process and combine chunks
        processed_audio = sum([process_chunks(chunk, MIN_SILENCE_LEN, SILENCE_THRESHOLD) for chunk in make_chunks(audio, CHUNK_LENGTH_MS)])
        processed_wav_path = os.path.join(PROCESSED_DIR, f"{filename}.wav")
        processed_audio.export(processed_wav_path, format="wav")

        # Load Whisper model and transcribe
        model = whisper.load_model("large", device="cuda" if torch.cuda.is_available() else "cpu")
        transcription = transcribe_audio(model, processed_wav_path)
        # Save transcription and convert to PDF
        pdf_path = save_audio_transcription_to_pdf(transcription, filename, PROCESSED_DIR)

        print(f"Processed transcription saved as PDF: {pdf_path}")
        print(f"Processing time: {time.time() - start_time:.2f} seconds")

        return pdf_path
    except Exception as e:
        raise

# --- Entry Point ---
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python audio_process.py <audio_path>")
        sys.exit(1)
    process_audio(sys.argv[1])