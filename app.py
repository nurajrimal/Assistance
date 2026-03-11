#!/usr/bin/env python3
# ============================================================
#  app.py  —  Mitra Web UI (Flask server)
#  Run: python app.py
#  Open: http://localhost:5000
# ============================================================

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import tempfile
import base64

from assistant_brain import get_response
from text_to_speech import clean_text_for_speech
from gtts import gTTS
from config import TTS_LANGUAGE

app = Flask(__name__, static_folder="web")
CORS(app)

# In-memory conversation history per session (simple, no DB needed)
conversation_history = []


@app.route("/")
def index():
    return send_from_directory("web", "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history
    data = request.get_json()
    user_text = data.get("text", "").strip()

    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    # Get response from brain
    reply = get_response(user_text, conversation_history)

    # Update history
    conversation_history.append({"role": "user", "content": user_text})
    conversation_history.append({"role": "assistant", "content": reply})
    if len(conversation_history) > 12:
        conversation_history = conversation_history[-12:]

    # Generate TTS audio and return as base64
    audio_b64 = None
    try:
        clean = clean_text_for_speech(reply)
        if clean:
            tts = gTTS(text=clean, lang=TTS_LANGUAGE, slow=False)
            tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            tts.save(tmp.name)
            with open(tmp.name, "rb") as f:
                audio_b64 = base64.b64encode(f.read()).decode("utf-8")
            os.unlink(tmp.name)
    except Exception as e:
        print(f"TTS error: {e}")

    return jsonify({"reply": reply, "audio": audio_b64})


@app.route("/reset", methods=["POST"])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({"status": "reset"})


if __name__ == "__main__":
    os.makedirs("web", exist_ok=True)
    print("\n🌐 मित्र Web UI सुरु हुँदैछ...")
    print("👉 Open in browser: http://localhost:5000\n")
    app.run(debug=False, port=5000, host='0.0.0.0')
