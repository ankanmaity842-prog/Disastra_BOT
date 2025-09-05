from flask import Flask, request, jsonify, render_template
from modules.query_handler import handle_query
from modules.language_support import detect_language, normalize_mixed_input
import json, os, random, time
from functools import lru_cache

app = Flask(__name__, static_folder="static", template_folder="templates")

static_folder = app.static_folder or "static"
dq_path = os.path.join(static_folder, "disaster_queries.json")

dq_data = {}
if os.path.exists(dq_path):
    with open(dq_path, "r", encoding="utf-8") as f:
        dq_data = json.load(f)

disaster_queries = dq_data.get("disaster_queries", {})
keyword_index = {}

for dtype, data in disaster_queries.items():
    followups = data.get("followups", {}).get("keyword", [])
    for block in followups:
        for kw in block.get("keywords", []):
            keyword_index.setdefault(kw.lower(), []).extend(block.get("messages", []))

intro_phrases = [
    "Great! Let’s take the next step together.",
    "I’m here with you. Want to keep going?",
    "Let’s make this simple and clear together.",
    "Here’s something that might really help.",
    "Want to explore this a bit more?",
    "Can I show you something helpful?",
    "Let me walk you through this.",
    "You’re on the right track. Want to go deeper?",
    "Let’s make this easier together.",
    "I’ve got something useful for you.",
    "Shall we dive into the next part?",
    "Let’s stay safe and smart. Want to hear more?",
    "I’ve got your back. Want to take a closer look?",
    "This might be useful — shall we explore it?",
    "Let’s walk through it step by step.",
    "Here’s something that could make things clearer.",
    "I’ve got a tip that might make this easier.",
    "You're doing great — ready for the next tip?",
    "Let’s take this one step further."
]

def detect_disaster_type(message: str):
    msg = normalize_mixed_input(message).lower()
    if "earthquake" in msg:
        return "earthquake"
    if "flood" in msg:
        return "flood"
    if "fire" in msg:
        return "fire"
    if "cyclone" in msg:
        return "cyclone"
    return None

@lru_cache(maxsize=500)
def cached_query(message, lang):
    return handle_query(message, lang)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_input = data.get("message", "").strip()
    user_lang = data.get("language", "").strip()

    if not user_input:
        return jsonify({"response": "Please enter a message.", "followup": None})

    if not user_lang:
        user_lang = detect_language(user_input)

    start_time = time.time()
    response = cached_query(user_input, user_lang)
    latency = round(time.time() - start_time, 2)

    disaster_type = detect_disaster_type(user_input)
    followup = None
    matched_messages = []

    normalized_input = normalize_mixed_input(user_input)
    for word in normalized_input.split():
        if word in keyword_index:
            matched_messages.extend(keyword_index[word])

    if not matched_messages and disaster_type:
        fallback_blocks = disaster_queries.get(disaster_type, {}).get("followups", {}).get("keyword", [])
        if fallback_blocks:
            fallback_block = random.choice(fallback_blocks)
            matched_messages.extend(random.sample(
                fallback_block.get("messages", []),
                min(3, len(fallback_block.get("messages", [])))
            ))

    if matched_messages:
        intro = random.choice(intro_phrases)
        followup = f"{intro} {random.choice(matched_messages)}"

    return jsonify({
        "response": response,
        "followup": followup,
        "latency": f"{latency}s"
    })

if __name__ == "__main__":
    app.run(debug=True)