import torch
from pydub import AudioSegment
from pydub.silence import detect_silence
from pydub.utils import make_chunks
import noisereduce as nr
import numpy as np
import whisper




def process_chunks(chunk, min_silence_len, silence_threshold):
    """Reduce noise and trim silence from an audio chunk."""
    print("CHUNK", chunk)
    reduced_chunk = nr.reduce_noise(y=np.array(chunk.get_array_of_samples()), 
                                    sr=chunk.frame_rate, prop_decrease=0.8)
    print("REDUCED", reduced_chunk)
    audio = AudioSegment(reduced_chunk.tobytes(), frame_rate=chunk.frame_rate, 
                         sample_width=chunk.sample_width, channels=chunk.channels)
    print("AUDIO", audio)

    # Trim silence
    silences = detect_silence(audio, min_silence_len=min_silence_len, 
                              silence_thresh=silence_threshold)
    print("SILENCES", silences)
    return audio[silences[0][0]:silences[-1][1]] if silences else audio

def transcribe_audio(model ,audio_path):
    print("HELLO")
    """Use Whisper model to transcribe audio."""

    return model.transcribe(audio_path, language="en", verbose=True)