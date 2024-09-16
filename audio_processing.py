import whisper
import numpy as np
from pydub import AudioSegment
from pydub.silence import detect_silence
from pydub.utils import make_chunks
import noisereduce as nr
from multiprocessing import Pool
from docx import Document
import torch
import os
import sys

def process_chunk(chunk):
    chunk_np = np.array(chunk.get_array_of_samples())
    reduced_chunk = nr.reduce_noise(y=chunk_np, sr=chunk.frame_rate, prop_decrease=0.8)

    reduced_chunk_audio = AudioSegment(
        reduced_chunk.tobytes(), 
        frame_rate=chunk.frame_rate, 
        sample_width=chunk.sample_width, 
        channels=chunk.channels
    )

    silences = detect_silence(reduced_chunk_audio, min_silence_len=1000, silence_thresh=-30)
    if silences:
        start_trim, end_trim = silences[0][0], silences[-1][1]
        return reduced_chunk_audio[start_trim:end_trim]
    return reduced_chunk_audio

def process_audio(audio_path):
    # chunk_length_ms = 300000
    chunk_length_ms = 120000
    audio = AudioSegment.from_file(audio_path)
    filename = audio_path.split('/')[-1]
    filename = filename.split('.')[0]

        processed_wav_path = os.path.join('processed', f"{filename}.wav")
        original_docx_path = os.path.join('processed', f"{filename}-original.docx")
        processed_docx_path = os.path.join('processed', f"{filename}-processed.docx")

        # Ensure files do not already exist
        if os.path.exists(processed_wav_path):
            os.remove(processed_wav_path)
            logging.info(f"Removed existing file: {processed_wav_path}")

        if os.path.exists(original_docx_path):
            os.remove(original_docx_path)
            logging.info(f"Removed existing file: {original_docx_path}")

        if os.path.exists(processed_docx_path):
            os.remove(processed_docx_path)
            logging.info(f"Removed existing file: {processed_docx_path}")


    chunks = make_chunks(audio, chunk_length_ms)

    with Pool() as pool:
        processed_chunks = pool.map(process_chunk, chunks)

    combined_audio = sum(processed_chunks)

    combined_audio.export(f"./processed/{filename}.wav", format="wav")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("large", device=device)

    print("Transcription of processed audio:")
    result = model.transcribe(f"./processed/{filename}.wav", language="en", verbose=True)

    document = Document()
    document.add_heading('Transcription of processed audio:', level=1)
    document.add_paragraph(result["text"])
    document.save(f'./processed/{filename}-processed.docx')

    print(' ')

    print("Transcription of original audio:")
    result_original = model.transcribe(audio_path, language="en", verbose=True)
    original_document = Document()
    original_document.add_heading('Transcription of original audio:', level=1)
    original_document.add_paragraph(result_original["text"])
    original_document.save(f'./processed/{filename}-original.docx')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python audio_process.py <audio_path>")
        sys.exit(1)
    audio_path = sys.argv[1]
    process_audio(audio_path)