from modules.language_support import normalize_mixed_input

def get_context(user_input):
    normalized = normalize_mixed_input(user_input)

    if "earthquake" in normalized:
        return "You are a disaster management expert helping students prepare for earthquakes."
    elif "flood" in normalized:
        return "You are a disaster management expert helping students prepare for floods."
    elif "fire" in normalized:
        return "You are a disaster management expert helping students prepare for fires."
    elif "cyclone" in normalized:
        return "You are a disaster management expert helping students prepare for cyclones."
    else:
        return "You are a general disaster preparedness assistant for students."