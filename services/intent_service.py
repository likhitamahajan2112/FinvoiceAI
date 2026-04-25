from rapidfuzz import process

INTENTS = {
    "login": ["login", "log in", "sign in"],
    "balance": ["balance", "check balance", "show balance", "account balance", "what is my balance"],
    "transactions": ["transactions", "recent transactions", "show transactions", "account history"],
    "transfer": ["transfer", "send money", "transfer funds", "make payment"],
    "logout": ["logout", "log out", "sign out"],
    "confirm": ["yes", "confirm", "okay", "proceed"],
    "cancel": ["no", "cancel", "stop", "abort"],
    "exit": ["exit", "quit", "stop", "goodbye"]
}

def classify_intent(transcript):
    transcript = transcript.lower()
    all_phrases = []
    for intent, phrases in INTENTS.items():
        for phrase in phrases:
            all_phrases.append((phrase, intent))

    match, score, intent = None, 0, "unknown"
    for phrase, intent_key in all_phrases:
        result = process.extractOne(transcript, [phrase])
        if result and result[1] > score and result[1] >= 70:
            match, score, intent = result[0], result[1], intent_key
    return intent