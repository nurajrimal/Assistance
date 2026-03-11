# ============================================================
#  assistant_brain.py  —  The "brain": understands & responds
#  Uses Google Gemini API (new google.genai package)
# ============================================================

import re
import datetime
from google import genai
from google.genai import types
from colorama import Fore, Style
from config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPT, ASSISTANT_NAME


# ── Built-in rules (fast, no API needed) ─────────────────────

BUILTIN_RESPONSES = {
    r"समय|time|बज्यो|clock":             lambda: _get_time(),
    r"मिति|date|आजको|today":             lambda: _get_date(),
    r"नमस्ते|नमस्कार|hello|hi\b|hey":   lambda: f"नमस्ते! म {ASSISTANT_NAME} हुँ। आज तपाईंको के सहायता गर्न सक्छु? 😊",
    r"तिम्रो नाम|your name|तपाईंको नाम": lambda: f"मेरो नाम {ASSISTANT_NAME} हो। म तपाईंको नेपाली AI सहायक हुँ। 🤖",
    r"राजधानी|capital":                  lambda: "नेपालको राजधानी काठमाडौं हो। 🏔️",
    r"जनसंख्या|population":              lambda: "नेपालको जनसंख्या लगभग ३ करोड छ। 📊",
    r"जोक|joke|मजाक|हाँसो":             lambda: _get_joke(),
    r"धन्यवाद|thank|सुक्रिया":           lambda: "स्वागत छ! अरू केही सहायता चाहियो भने सोध्नुस्। 🙏",
    r"बाई|bye|विदाई|अलविदा":             lambda: "फेरि भेटौंला! शुभकामना। 🙏",
    r"कस्तो छ|कस्तो हुनुहुन्छ|how are you": lambda: "म ठीक छु, धन्यवाद! तपाईं कस्तो हुनुहुन्छ? 😊",
    r"नेपाल.*बारे|about nepal":          lambda: "नेपाल दक्षिण एशियामा अवस्थित एक सुन्दर पहाडी देश हो। सगरमाथा (८,८४९ मिटर) यहीं छ। 🏔️",
}


def _get_time() -> str:
    now = datetime.datetime.now()
    period = "बिहान" if now.hour < 12 else ("दिउँसो" if now.hour < 17 else "साँझ")
    return f"अहिले {period} {now.strftime('%I')}:{now.strftime('%M')} बजेको छ। ⏰"


def _get_date() -> str:
    now = datetime.datetime.now()
    days = ["सोमबार","मंगलबार","बुधबार","बिहीबार","शुक्रबार","शनिबार","आइतबार"]
    months = ["जनवरी","फेब्रुअरी","मार्च","अप्रिल","मई","जुन",
              "जुलाई","अगस्ट","सेप्टेम्बर","अक्टोबर","नोभेम्बर","डिसेम्बर"]
    return f"आज {days[now.weekday()]}, {now.day} {months[now.month-1]} {now.year} हो। 📅"


def _get_joke() -> str:
    import random
    jokes = [
        "एकपटक एउटा कम्प्युटरले गाना गाउन थाल्यो — बाइट-बाइट सुनिन्थ्यो! 😄",
        "प्रोग्रामरलाई किन जंगल मन पर्छ? किनभने त्यहाँ धेरै 'tree structure' हुन्छ! 🌲",
        "Python programmer ले किन coffee पिउँछन्? किनभने Java मन पर्दैन! ☕",
    ]
    return random.choice(jokes)


# ── Gemini client ─────────────────────────────────────────────

_client = None

def _get_client():
    global _client
    if _client is None:
        if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_key_here":
            return None
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


# ── Main brain function ───────────────────────────────────────

def get_response(user_text: str, conversation_history: list = None) -> str:
    if not user_text.strip():
        return "मैले तपाईंको कुरा बुझिनँ। कृपया फेरि भन्नुहोस्।"

    text_lower = user_text.lower()

    # 1. Fast built-in responses
    for pattern, response_fn in BUILTIN_RESPONSES.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            print(f"{Fore.MAGENTA}💡 Built-in response.{Style.RESET_ALL}")
            return response_fn()

    # 2. Gemini API
    print(f"{Fore.CYAN}🧠 Gemini सोच्दैछ...{Style.RESET_ALL}")
    return _call_gemini(user_text, conversation_history or [])


def _call_gemini(user_text: str, history: list) -> str:
    client = _get_client()
    if client is None:
        return "API key राखिएको छैन। .env फाइलमा GEMINI_API_KEY थप्नुहोस्।"

    try:
        # Build contents from history + new message
        contents = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))
        contents.append(types.Content(role="user", parts=[types.Part(text=user_text)]))

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=300,
            )
        )
        return response.text.strip()

    except Exception as e:
        err = str(e).lower()
        if "api_key" in err or "invalid" in err:
            return "Gemini API key गलत छ। .env फाइल जाँच गर्नुहोस्।"
        if "quota" in err or "limit" in err:
            return "API limit पुग्यो। केही बेर पर्खनुहोस्।"
        print(f"{Fore.RED}❌ Gemini त्रुटि: {e}{Style.RESET_ALL}")
        return "माफ गर्नुस्, अहिले जवाफ दिन सकिएन।"


if __name__ == "__main__":
    print("🧠 Brain test (type 'quit' to exit)\n")
    history = []
    while True:
        user = input("तपाईं: ")
        if user.lower() == "quit":
            break
        reply = get_response(user, history)
        print(f"मित्र: {reply}\n")
        history.append({"role": "user", "content": user})
        history.append({"role": "assistant", "content": reply})