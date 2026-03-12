# 🎙️ मित्र — Nepali Voice Assistant

A full Python voice assistant that understands and speaks Nepali.

```
Your Voice → Whisper (STT) → AI (Brain) → gTTS (TTS) → Nepali Audio
```

---

## 📁 Project Structure

```
mitra_assistant/
│
├── main.py              ← Run this to start
├── config.py            ← All settings (model, language, etc.)
├── record_audio.py      ← Microphone → WAV file
├── speech_to_text.py    ← WAV → Nepali text (Whisper)
├── assistant_brain.py   ← Text → Smart response (Claude AI)
├── text_to_speech.py    ← Text → Nepali speech (gTTS)
├── logger.py            ← Saves conversations to file
├── requirements.txt     ← Python dependencies
├── .env                 ← Your API keys (keep private!)
│
├── audio/               ← Auto-created: temp audio files
└── logs/                ← Auto-created: conversation logs
```

---

## ⚡ Quick Setup (5 minutes)

### Step 1 — Install Python dependencies

```bash
pip install -r requirements.txt
```

If `pyaudio` fails on Windows:
```bash
pip install pipwin
pipwin install pyaudio
```

If `pyaudio` fails on Mac:
```bash
brew install portaudio
pip install pyaudio
```

### Step 2 — Add your API key

Open `.env` and replace the placeholder:
```
ANTHROPIC_API_KEY=your_actual_key_here
```

Get a free key at: https://console.anthropic.com

### Step 3 — Run it!

**Voice mode** (full experience):
```bash
python main.py
```

**Text mode** (no microphone needed, great for testing):
```bash
python main.py --text
```

---

## 🎮 How to Use

### Voice Mode
1. Run `python main.py`
2. Wait for "मित्र तयार छ!" message
3. Press **Enter** to start recording
4. Speak in Nepali
5. Mitra responds in Nepali (text + audio)
6. Say "बाई" or press Ctrl+C to quit

### Text Mode
1. Run `python main.py --text`
2. Type in Nepali (or English)
3. See + hear the response
4. Type `quit` to exit

---

## 💬 Example Conversations

```
तपाईं: नमस्ते!
मित्र: नमस्ते! म मित्र हुँ। आज तपाईंको के सहायता गर्न सक्छु? 😊

तपाईं: समय कति भयो?
मित्र: अहिले बिहान १०:३५ बजेको छ। ⏰

तपाईं: नेपालको राजधानी के हो?
मित्र: नेपालको राजधानी काठमाडौं हो। 🏔️

तपाईं: एउटा जोक सुनाउ
मित्र: Python programmer ले किन coffee पिउँछन्? किनभने Java मन पर्दैन! ☕

तपाईं: AI को भविष्य कस्तो छ?
मित्र: [Claude AI ले जवाफ दिन्छ]
```

---

## ⚙️ Configuration (config.py)

| Setting | Default | Description |
|---------|---------|-------------|
| `WHISPER_MODEL` | `"small"` | `tiny/base/small/medium/large` |
| `WHISPER_LANGUAGE` | `"ne"` | Nepali |
| `RECORD_SECONDS` | `6` | Max recording duration |
| `TTS_LANGUAGE` | `"ne"` | Nepali TTS |
| `RECORD_SECONDS` | `6` | Seconds per recording |

**Whisper model guide:**
- `tiny` — Fastest, works offline, less accurate
- `small` — ✅ Best for Nepali (recommended)
- `medium` — More accurate, slower
- `large` — Most accurate, needs GPU

---

## 🛠️ Troubleshooting

**"No module named pyaudio"**
```bash
# Windows
pip install pipwin && pipwin install pyaudio
# Mac
brew install portaudio && pip install pyaudio
# Linux
sudo apt install portaudio19-dev && pip install pyaudio
```

**"API key राखिएको छैन"**
→ Open `.env` file and add your Anthropic API key

**Audio not playing on Linux**
```bash
sudo apt install mpg123
```

**Whisper model downloading slowly**
→ Normal on first run. `small` model = ~460MB. Downloaded once, cached forever.

---

## 🚀 Next Steps (Upgrade Ideas)

- [ ] Wake word detection ("हे मित्र" → starts listening automatically)
- [ ] Weather API integration (OpenWeather)
- [ ] Web UI with Flask/Gradio
- [ ] Nepali calendar (Bikram Sambat)
- [ ] WhatsApp/Telegram bot integration
- [ ] Custom voice training with Coqui TTS

---

## 📦 Tech Stack

| Component | Library | Why |
|-----------|---------|-----|
| Speech-to-Text | OpenAI Whisper | Best Nepali accuracy |
| AI Brain | Anthropic Claude | Nepali language understanding |
| Text-to-Speech | gTTS (Google) | Free, good Nepali voice |
| Audio Recording | sounddevice | Cross-platform, reliable |
| Terminal colors | colorama | Windows-compatible colors |
