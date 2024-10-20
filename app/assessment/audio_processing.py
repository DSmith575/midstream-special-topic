import os
import gc
import tempfile
import sys
from pydub import AudioSegment
from pydub.utils import make_chunks
import time
from app.constants import PROCESSED_DIR, CHUNK_LENGTH_MS, SILENCE_THRESHOLD, MIN_SILENCE_LEN, PROCESSED_FOLDER
from app.audioHelpers import process_chunks
from app.documentProcessing import save_audio_transcription_to_pdf
from app.chatgptCompletions import process_client_audio

def process_audio(audio_path):
    """Main processing function: chunk audio, process, transcribe, and convert."""
    try:
        start_time = time.time()
        audio = AudioSegment.from_file(audio_path)
        filename = os.path.splitext(os.path.basename(audio_path))[0]
        full_transcription = ""

        # Process each chunk
        for i, chunk in enumerate(make_chunks(audio, CHUNK_LENGTH_MS)):
            processed_chunk = process_chunks(chunk, MIN_SILENCE_LEN, SILENCE_THRESHOLD)
            with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as temp_chunk_file:
                processed_chunk.export(temp_chunk_file.name, format="wav")
                transcription = process_client_audio(temp_chunk_file.name)
                full_transcription += transcription + "\n\n"

            gc.collect()  # Call garbage collector
        
        print(f"Processing time: {time.time() - start_time} seconds")
        print(f"Full transcription: {full_transcription}")
        pdf_path = save_audio_transcription_to_pdf(full_transcription, filename, PROCESSED_FOLDER)
        return pdf_path
    except Exception as e:
        print(f"Error in processing audio: {e}")
        raise

# --- Entry Point ---
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python audio_process.py <audio_path>")
        sys.exit(1)
    process_audio(sys.argv[1])