from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator
import re

DetectorFactory.seed = 0

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def normalize_mixed_input(text):
    text = text.strip().lower()

    filler_words = [
        "ke", "ka", "ki", "hai", "ho", "hota", "hoti", "par", "mein", "me", "toh", "tha", "thi", "raha", "rahi"
    ]
    for word in filler_words:
        text = re.sub(rf"\b{word}\b", "", text)

    replacements = {
        "bhukamp": "earthquake",
        "aag": "fire",
        "baarish": "rain",
        "baadh": "flood",
        "bavandar": "cyclone",
        "jaldi": "quickly",
        "madad": "help",
        "bachaao": "rescue",
        "kya karna chahiye": "what should we do",
        "kya karein": "what should I do",
        "baj gaya": "started",
        "baj jaaye": "goes off",
        "alarm": "alarm",
        "hostel": "hostel",
        "school": "school",
        "classroom": "classroom"
    }

    for local, english in replacements.items():
        text = text.replace(local, english)

    text = re.sub(r"\s+", " ", text)
    return text

def translate_input(text, lang):
    try:
        return GoogleTranslator(source=lang, target='en').translate(text)
    except:
        return text

def translate_output(text, lang):
    try:
        return GoogleTranslator(source='en', target=lang).translate(text)
    except:
        return text