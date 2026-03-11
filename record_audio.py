# ============================================================
#  record_audio.py  —  Captures voice from microphone
# ============================================================

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os
from colorama import Fore, Style
from config import SAMPLE_RATE, RECORD_SECONDS, SILENCE_THRESHOLD, CHANNELS


def record_audio(duration: int = RECORD_SECONDS) -> str:
    """
    Record audio from the microphone.
    Returns the path to a temporary WAV file.
    """
    print(f"{Fore.CYAN}🎙️  सुन्दैछु... ({duration} सेकेन्ड){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   बोल्नुहोस् — Speak now...{Style.RESET_ALL}")

    try:
        # Record audio
        recording = sd.rec(
            int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16"
        )
        sd.wait()  # Wait until recording is done

        # Check if there's actual audio (not just silence)
        volume = np.abs(recording).mean()
        if volume < 100:
            print(f"{Fore.RED}⚠️  कुनै आवाज सुनिएन। पुनः प्रयास गर्नुहोस्।{Style.RESET_ALL}")
            return None

        # Save to temp WAV file
        tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        wav.write(tmp_file.name, SAMPLE_RATE, recording)
        print(f"{Fore.GREEN}✅  रेकर्डिङ सकियो।{Style.RESET_ALL}")
        return tmp_file.name

    except Exception as e:
        print(f"{Fore.RED}❌  माइक्रोफोन त्रुटि: {e}{Style.RESET_ALL}")
        print(f"    सुनिश्चित गर्नुहोस् कि माइक्रोफोन जडान छ।")
        return None


def record_with_silence_detection(max_duration: int = RECORD_SECONDS) -> str:
    """
    Advanced: Record until silence is detected (stops early).
    Good for natural conversation flow.
    """
    print(f"{Fore.CYAN}🎙️  सुन्दैछु... (बोल्न सकिए रोकिनेछ){Style.RESET_ALL}")

    chunk_size = 1024
    recorded_chunks = []
    silence_count = 0
    max_silence_chunks = int(SAMPLE_RATE / chunk_size * 1.5)  # 1.5s silence = stop

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="int16") as stream:
        print(f"{Fore.YELLOW}   बोल्नुहोस्...{Style.RESET_ALL}", end="", flush=True)
        total_chunks = int(SAMPLE_RATE * max_duration / chunk_size)

        for _ in range(total_chunks):
            chunk, _ = stream.read(chunk_size)
            recorded_chunks.append(chunk.copy())

            # Detect silence
            volume = np.abs(chunk).mean()
            if volume < SILENCE_THRESHOLD:
                silence_count += 1
                print(".", end="", flush=True)
            else:
                silence_count = 0
                print("█", end="", flush=True)

            # Stop if silence detected after speaking
            if silence_count > max_silence_chunks and len(recorded_chunks) > 10:
                break

    print()  # newline

    recording = np.concatenate(recorded_chunks, axis=0)

    if np.abs(recording).mean() < 100:
        print(f"{Fore.RED}⚠️  कुनै आवाज सुनिएन।{Style.RESET_ALL}")
        return None

    tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wav.write(tmp_file.name, SAMPLE_RATE, recording)
    print(f"{Fore.GREEN}✅  रेकर्डिङ सकियो।{Style.RESET_ALL}")
    return tmp_file.name


def cleanup_audio_file(filepath: str):
    """Delete temporary audio file."""
    if filepath and os.path.exists(filepath):
        os.remove(filepath)


if __name__ == "__main__":
    # Test recording
    print("🔴 Recording test...")
    path = record_audio(duration=4)
    if path:
        print(f"✅ Saved to: {path}")
        cleanup_audio_file(path)
