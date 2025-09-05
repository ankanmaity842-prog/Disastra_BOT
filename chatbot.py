from modules.query_handler import handle_query
from modules.language_support import translate_input, translate_output

def chat():
    print("🌐 Welcome to DisastraBot!")
    user_lang = input("Choose your language (e.g., English, Hindi, Bengali, Tamil, Telugu): ").strip()

    print("Type 'exit' to leave.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        translated_input = translate_input(user_input, user_lang)
        response = handle_query(translated_input, user_lang)
        final_response = translate_output(response, user_lang)

        print(f"DisastraBot: {final_response}")

if __name__ == "__main__":
    chat()