# ============================================================
#  text_to_speech.py  —  Converts Nepali text → spoken audio
# ============================================================

import os
import sys
import re
from gtts import gTTS
from colorama import Fore, Style
from config import TTS_LANGUAGE, TTS_SLOW, AUDIO_OUTPUT_FILE


def clean_text_for_speech(text: str) -> str:
    """Remove emojis and special chars before TTS."""
    # Remove emojis
    emoji_pattern = re.compile(
        "[\U00010000-\U0010ffff"
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\u2600-\u26FF\u2700-\u27BF]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub("", text)
    # Remove extra spaces
    text = " ".join(text.split())
    return text.strip()


def speak(text: str, output_file: str = AUDIO_OUTPUT_FILE):
    """
    Convert text to Nepali speech and play it.
    
    Args:
        text: Nepali text to speak
        output_file: Where to save the MP3
    """
    clean = clean_text_for_speech(text)
    if not clean:
        return

    print(f"{Fore.BLUE}🔊 बोल्दैछु...{Style.RESET_ALL}")

    try:
        # Generate speech
        tts = gTTS(text=clean, lang=TTS_LANGUAGE, slow=TTS_SLOW)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        tts.save(output_file)

        # Play the audio
        _play_audio(output_file)

    except Exception as e:
        print(f"{Fore.RED}❌ TTS त्रुटि: {e}{Style.RESET_ALL}")
        # Fallback: just print the text
        print(f"{Fore.YELLOW}📢 {text}{Style.RESET_ALL}")


def _play_audio(filepath: str):
    """Play audio file — handles Windows, Mac, Linux."""
    try:
        # Try playsound first
        from playsound import playsound
        playsound(filepath)
        return
    except ImportError:
        pass
    except Exception:
        pass

    # Platform fallback
    platform = sys.platform
    if platform == "win32":
        os.system(f'start /wait "" "{filepath}"')
    elif platform == "darwin":
        os.system(f'afplay "{filepath}"')
    else:
        # Linux: try multiple players
        for player in ["mpg123", "mpg321", "ffplay -nodisp -autoexit", "aplay"]:
            if os.system(f"which {player.split()[0]} > /dev/null 2>&1") == 0:
                os.system(f'{player} "{filepath}" > /dev/null 2>&1')
                return
        print(f"{Fore.YELLOW}⚠️  Audio player फेला परेन। `mpg123` install गर्नुहोस्: sudo apt install mpg123{Style.RESET_ALL}")


def speak_greeting():
    """Play startup greeting."""
    speak("नमस्ते! म मित्र हुँ। म तपाईंको नेपाली सहायक हुँ। के गर्न सक्छु?")


if __name__ == "__main__":
    # Test TTS
    test = sys.argv[1] if len(sys.argv) > 1 else "नमस्ते! म मित्र हुँ।"
    speak(test)
