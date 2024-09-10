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

def process_audio():
    # chunk_length_ms = 300000
    chunk_length_ms = 120000
    audio = AudioSegment.from_file("./Audio/Deacon.m4a")
    # audio = AudioSegment.from_file("./Audio/switch.mp4")

    trimmed_path = "./TrimmedAudio/Deacon_trimmed.wav"
    if os.path.exists(trimmed_path):
        os.remove(trimmed_path)
        print("File deleted")

    file_transcription = "./Transcription-original.docx"
    if os.path.exists(file_transcription):
        os.remove(file_transcription)
        print("File deleted")

    file_processed_transcription = "./Transcription-processed.docx"
    
    if os.path.exists(file_processed_transcription):
        os.remove(file_processed_transcription)
        print("File deleted")



    chunks = make_chunks(audio, chunk_length_ms)

    with Pool() as pool:
        processed_chunks = pool.map(process_chunk, chunks)

    combined_audio = sum(processed_chunks)

    combined_audio.export("./TrimmedAudio/Deacon_trimmed.wav", format="wav")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("large", device=device)

    result = model.transcribe("./TrimmedAudio/Deacon_trimmed.wav", language="en", verbose=True)
    print("Transcription of processed audio:")

    document = Document()
    document.add_heading('Transcription of processed audio:', level=1)
    document.add_paragraph(result["text"])
    document.save('Transcription-processed.docx')

    result_original = model.transcribe("./Audio/Deacon.m4a", language="en", verbose=False)
    original_document = Document()
    original_document.add_heading('Transcription of original audio:', level=1)
    original_document.add_paragraph(result_original["text"])
    original_document.save('Transcription-original.docx')

if __name__ == '__main__':
    process_audio()