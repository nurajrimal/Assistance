# ============================================================
#  config.py  —  Mitra Nepali Voice Assistant
#  All settings in one place. Edit this file to customize.
# ============================================================

import os
from dotenv import load_dotenv

load_dotenv()

# ── API Keys ─────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# ── Gemini Model ─────────────────────────────────────────────
# Options: gemini-1.5-flash (fast & free) | gemini-1.5-pro (smarter)
GEMINI_MODEL = "gemini-2.0-flash"

# ── Whisper (Speech-to-Text) ─────────────────────────────────
WHISPER_MODEL = "small"
WHISPER_LANGUAGE = "ne"

# ── Recording ────────────────────────────────────────────────
SAMPLE_RATE = 16000
RECORD_SECONDS = 6
SILENCE_THRESHOLD = 500
CHANNELS = 1

# ── Text-to-Speech (gTTS) ────────────────────────────────────
TTS_LANGUAGE = "ne"
TTS_SLOW = False
AUDIO_OUTPUT_FILE = "audio/response.mp3"

# ── Assistant Personality ────────────────────────────────────
ASSISTANT_NAME = "मित्र"
SYSTEM_PROMPT = """तपाईं "मित्र" हुनुहुन्छ — एक मित्रवत, चलाख नेपाली AI सहायक।

नियमहरू:
- सधैं नेपाली भाषामा जवाफ दिनुहोस्
- छोटो र स्पष्ट जवाफ दिनुहोस् (२-३ वाक्य)
- मित्रवत र सकारात्मक स्वरमा बोल्नुहोस्
- यदि थाहा छैन भने इमानदारीसाथ भन्नुहोस्"""

# ── Logging ──────────────────────────────────────────────────
LOG_FILE = "logs/conversation.log"
LOG_CONVERSATIONS = True
