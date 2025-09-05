import os
import time
from dotenv import load_dotenv
from modules.language_support import (
    translate_input,
    translate_output,
    detect_language,
    normalize_mixed_input
)
from modules.context_manager import get_context
from modules.student_queries import enrich_student_query
from google.generativeai.client import configure
from google.generativeai.generative_models import GenerativeModel

load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))
model = GenerativeModel(model_name="gemini-2.5-flash")

def handle_query(user_input, user_lang):
    start_time = time.time()

    mixed_input = normalize_mixed_input(user_input)
    detected_lang = detect_language(mixed_input)
    translated_input = (
        mixed_input if detected_lang == user_lang
        else translate_input(mixed_input, detected_lang)
    )

    context = get_context(translated_input)
    enriched = enrich_student_query(translated_input)

    prompt = (
        f"{context}\n"
        f"{enriched}\n"
        f"Show respone in one to 3 lines for definition,first aid,kit,regions,global data,place,time like questions.Exclude bullet points for specific question like this.\n"
        f"Respond in 5 to 7 short bullet points as required. Exclude asterisks. Use simple, student-friendly language.\n"
        f"Most important point on the first, rest others.\n"
        f"Show response only for the disaster-related question including earthquake, flood, fire, cyclone.\n"
        f"Don't response on general question not related to disaster.\n"
        f"Be accurate and specific. Avoid general advice.\n"
        f"Show each point on the next line to previous point.\n"
        f"Respond briefly and precisely. Focus only on what the student needs to know.\n"
        f"Your task is to give a clear, accurate, and student-friendly answer.\n"
        f"Your task is to give response based on answers related to India.\n"
        f"Do not include introductions or conclusions.\n"
        f"User question (mixed language): {user_input}\n"
        f"Answer:"
    )

    try:
        response = model.generate_content(prompt)
        output = response.text.strip()
        final_output = (
            output if detected_lang == user_lang
            else translate_output(output, user_lang)
        )

        print(f"⏱️ Response time: {round(time.time() - start_time, 2)}s")
        return final_output

    except Exception as e:
        return f"⚠️ Unable to process your request: {str(e)}"