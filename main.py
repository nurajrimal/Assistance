#!/usr/bin/env python3
# ============================================================
#  main.py  —  Mitra: Nepali Voice Assistant
#  Run with: python main.py
#  Text-only mode: python main.py --text
# ============================================================

import sys
import os
from colorama import Fore, Back, Style, init

# Initialize colorama (for colored terminal output on Windows too)
init(autoreset=True)

# ── Banner ────────────────────────────────────────────────────
BANNER = f"""
{Fore.RED}╔══════════════════════════════════════════╗
║  {Fore.WHITE}  मित्र  —  Nepali Voice Assistant  {Fore.RED}   ║
║  {Fore.YELLOW}  Powered by Whisper + Gemini AI    {Fore.RED}   ║
╚══════════════════════════════════════════╝{Style.RESET_ALL}
"""


def run_voice_mode():
    """Full voice loop: record → transcribe → respond → speak."""
    from record_audio import record_with_silence_detection, record_audio, cleanup_audio_file
    from speech_to_text import transcribe_audio, load_model
    from assistant_brain import get_response
    from text_to_speech import speak, speak_greeting
    from logger import log, log_session_start

    print(BANNER)
    print(f"{Fore.YELLOW}⏳ प्रारम्भ हुँदैछ... (Whisper model लोड हुँदैछ){Style.RESET_ALL}\n")

    # Pre-load Whisper model (so first response isn't slow)
    load_model()

    log_session_start()
    speak_greeting()

    conversation_history = []
    print(f"\n{Fore.GREEN}✅ मित्र तयार छ! कुरा गर्न Enter थिच्नुहोस्। 'बाई' भन्नुस् वा Ctrl+C गरी बन्द गर्नुस्।{Style.RESET_ALL}\n")

    while True:
        try:
            # Wait for user to press Enter before recording
            input(f"{Fore.CYAN}▶  कुरा गर्न Enter थिच्नुहोस्...{Style.RESET_ALL}")

            # Step 1: Record audio
            audio_path = record_with_silence_detection()
            if not audio_path:
                continue

            # Step 2: Speech → Text
            user_text = transcribe_audio(audio_path)
            cleanup_audio_file(audio_path)

            if not user_text:
                speak("माफ गर्नुस्, मैले सुन्न सकिनँ। फेरि भन्नुहोस्।")
                continue

            log("USER", user_text)

            # Exit condition
            if any(word in user_text.lower() for word in ["बाई", "अलविदा", "बन्द गर", "exit", "quit", "bye"]):
                speak("ठीक छ, बाई! भेटौंला। 🙏")
                log("MITRA", "Session ended.")
                break

            # Step 3: Get AI response
            reply = get_response(user_text, conversation_history)

            # Step 4: Show & speak response
            print(f"\n{Fore.RED}मित्र:{Style.RESET_ALL} {reply}\n")
            log("MITRA", reply)
            speak(reply)

            # Update conversation history (last 6 turns = 3 exchanges)
            conversation_history.append({"role": "user", "content": user_text})
            conversation_history.append({"role": "assistant", "content": reply})
            if len(conversation_history) > 12:
                conversation_history = conversation_history[-12:]

        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}👋 मित्र बन्द भयो। नमस्ते!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ त्रुटि: {e}{Style.RESET_ALL}")
            continue


def run_text_mode():
    """Text-only mode — no microphone needed. Great for testing."""
    from assistant_brain import get_response
    from text_to_speech import speak
    from logger import log, log_session_start

    print(BANNER)
    print(f"{Fore.CYAN}📝 Text mode — माइक्रोफोन बिना काम गर्छ।{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   'quit' टाइप गरेर बन्द गर्नुस्।{Style.RESET_ALL}\n")

    log_session_start()
    conversation_history = []

    while True:
        try:
            user_text = input(f"{Fore.GREEN}तपाईं: {Style.RESET_ALL}").strip()

            if not user_text:
                continue

            if user_text.lower() in ["quit", "exit", "bye", "बाई"]:
                print(f"\n{Fore.YELLOW}👋 बाई! भेटौंला।{Style.RESET_ALL}")
                break

            log("USER", user_text)

            reply = get_response(user_text, conversation_history)
            print(f"{Fore.RED}मित्र:{Style.RESET_ALL} {reply}\n")
            log("MITRA", reply)

            # Ask if user wants audio
            speak(reply)

            conversation_history.append({"role": "user", "content": user_text})
            conversation_history.append({"role": "assistant", "content": reply})
            if len(conversation_history) > 12:
                conversation_history = conversation_history[-12:]

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 बाई!{Style.RESET_ALL}")
            break


def check_setup():
    """Quick setup check before running."""
    issues = []

    # Check .env
    if not os.path.exists(".env"):
        issues.append("⚠️  .env file छैन। .env.example बाट copy गर्नुहोस्।")

    # Check API key
    from config import GEMINI_API_KEY
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_key_here":
        issues.append("⚠️  GEMINI_API_KEY .env मा राखिएको छैन। Built-in responses मात्र काम गर्नेछन्।")

    if issues:
        print(f"\n{Fore.YELLOW}Setup चेतावनीहरू:{Style.RESET_ALL}")
        for issue in issues:
            print(f"  {Fore.YELLOW}{issue}{Style.RESET_ALL}")
        print()


if __name__ == "__main__":
    check_setup()

    # Check for --text flag
    if "--text" in sys.argv or "-t" in sys.argv:
        run_text_mode()
    else:
        # Check if sounddevice is available
        try:
            import sounddevice
            run_voice_mode()
        except ImportError:
            print(f"{Fore.YELLOW}⚠️  sounddevice install भएको छैन। Text mode मा सुरु हुँदैछ।{Style.RESET_ALL}")
            print(f"   Voice mode का लागि: pip install sounddevice pyaudio\n")
            run_text_mode()
