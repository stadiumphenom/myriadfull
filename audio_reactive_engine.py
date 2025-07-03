import librosa
import numpy as np

def extract_audio_pulse(audio_path, num_frames, sr=22050):
    y, _ = librosa.load(audio_path, sr=sr)
    hop_length = len(y) // num_frames
    envelope = []

    for i in range(num_frames):
        start = i * hop_length
        end = min(start + hop_length, len(y))
        segment = y[start:end]
        amplitude = np.sqrt(np.mean(segment**2))
        envelope.append(amplitude)

    # Normalize to 0-1
    max_amp = max(envelope) or 1.0
    envelope = [min(amp / max_amp, 1.0) for amp in envelope]
    return envelope