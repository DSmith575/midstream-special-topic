from pydub import AudioSegment
from pydub.silence import detect_silence
import noisereduce as nr
import numpy as np

def process_chunks(chunk, min_silence_len, silence_threshold):
    try:
        """Reduce noise and trim silence from an audio chunk."""
        print("CHUNK", chunk)
        
        # Reduce noise and convert to NumPy array
        samples = np.array(chunk.get_array_of_samples())
        reduced_chunk = nr.reduce_noise(y=samples, sr=chunk.frame_rate, prop_decrease=0.8)
        
        # Create audio segment from reduced noise
        audio = AudioSegment(reduced_chunk.tobytes(), frame_rate=chunk.frame_rate, 
                             sample_width=chunk.sample_width, channels=chunk.channels)

        # Trim silence
        silences = detect_silence(audio, min_silence_len=min_silence_len, 
                                  silence_thresh=silence_threshold)
        print("SILENCES", silences)

        if silences:
            # Use slicing to avoid creating new AudioSegment unnecessarily
            start, end = silences[0][0], silences[-1][1]
            trimmed_audio = audio[start:end]
        else:
            trimmed_audio = audio

        # Clean up
        del samples  # Explicitly delete samples to free memory
        del reduced_chunk  # Free memory used by reduced_chunk
        return trimmed_audio

    except Exception as e:
        print(f"Error processing chunk: {e}")
        raise