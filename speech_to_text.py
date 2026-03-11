# ============================================================
#  speech_to_text.py  —  Converts Nepali audio → text (Whisper)
# ============================================================

import whisper
import os
from colorama import Fore, Style
from config import WHISPER_MODEL, WHISPER_LANGUAGE

# Load model once at startup (avoid reloading every time)
_model = None


def load_model():
    """Load Whisper model (called once)."""
    global _model
    if _model is None:
        print(f"{Fore.YELLOW}⏳ Whisper '{WHISPER_MODEL}' model लोड हुँदैछ...{Style.RESET_ALL}")
        _model = whisper.load_model(WHISPER_MODEL)
        print(f"{Fore.GREEN}✅ Whisper model तयार छ।{Style.RESET_ALL}")
    return _model


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe a WAV file to Nepali text using Whisper.
    
    Args:
        audio_path: Path to the WAV audio file
    
    Returns:
        Transcribed text string, or empty string on failure
    """
    if not audio_path or not os.path.exists(audio_path):
        print(f"{Fore.RED}❌ Audio file फेला परेन।{Style.RESET_ALL}")
        return ""

    try:
        model = load_model()
        print(f"{Fore.CYAN}🔄 ट्रान्सक्राइब गर्दैछु...{Style.RESET_ALL}")

        # Transcribe with Nepali language hint
        result = model.transcribe(
            audio_path,
            language=WHISPER_LANGUAGE,    # "ne" for Nepali
            fp16=False,                    # Use fp32 (safer for CPU)
            task="transcribe",             # "transcribe" keeps original language
                                           # Use "translate" to get English output
        )

        text = result["text"].strip()

        if text:
            print(f"{Fore.GREEN}🗣️  तपाईंले भन्नुभयो: {Fore.WHITE}{text}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️  बोली बुझिएन।{Style.RESET_ALL}")

        return text

    except Exception as e:
        print(f"{Fore.RED}❌ Transcription त्रुटि: {e}{Style.RESET_ALL}")
        return ""


def transcribe_and_translate(audio_path: str) -> dict:
    """
    Transcribe Nepali audio AND get English translation.
    Useful for debugging or bilingual apps.
    
    Returns:
        {"nepali": "...", "english": "..."}
    """
    model = load_model()

    nepali = model.transcribe(audio_path, language="ne", task="transcribe")
    english = model.transcribe(audio_path, language="ne", task="translate")

    return {
        "nepali": nepali["text"].strip(),
        "english": english["text"].strip()
    }


if __name__ == "__main__":
    # Test: transcribe a file passed as argument
    import sys
    if len(sys.argv) > 1:
        result = transcribe_audio(sys.argv[1])
        print(f"\nResult: {result}")
    else:
        print("Usage: python speech_to_text.py <audio_file.wav>")
