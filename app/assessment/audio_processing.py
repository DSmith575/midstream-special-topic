import os
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
        # Load audio and clean previous files
        audio = AudioSegment.from_file(audio_path)
        filename = os.path.splitext(os.path.basename(audio_path))[0]

        # Transcribe each processed chunk and combine transcriptions
        full_transcription = ""
        
        # Process each chunk
        for i, chunk in enumerate(make_chunks(audio, CHUNK_LENGTH_MS)):
            processed_chunk = process_chunks(chunk, MIN_SILENCE_LEN, SILENCE_THRESHOLD)
            
            # Export the processed chunk
            processed_chunk_path = os.path.join(PROCESSED_FOLDER, f"{filename}_chunk{i}.wav")
            processed_chunk.export(processed_chunk_path, format="wav")
            
            # Transcribe the processed chunk immediately
            try:
                transcription = process_client_audio(processed_chunk_path)
                full_transcription += transcription + "\n\n"
            except Exception as e:
                print(f"Error processing transcription for {processed_chunk_path}: {e}")
            
            # Clean up the processed chunk file immediately after transcription
            try:
                if os.path.exists(processed_chunk_path):
                    os.remove(processed_chunk_path)
                    print(f"Removed: {processed_chunk_path}")
                else:
                    print(f"File not found, skipping removal: {processed_chunk_path}")
            except Exception as e:
                print(f"Error removing {processed_chunk_path}: {e}")


        print(f"Processing time: {time.time() - start_time} seconds")
        print(f"Full transcription: {full_transcription}")
        # Save transcription and convert to PDF
        pdf_path = save_audio_transcription_to_pdf(full_transcription, filename, PROCESSED_FOLDER)
        return pdf_path
    except Exception as e:
        raise

# --- Entry Point ---
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python audio_process.py <audio_path>")
        sys.exit(1)
    process_audio(sys.argv[1])