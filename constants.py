import persona

AI_NAME = persona.selected_persona["name"]
PERSONA = {"role": "system", "content": persona.persona_description}
CHAT_HISTORY = [PERSONA]
DEFAULT_ERROR_MESSAGE = "Sorry, I can't answer now..."
LIMIT_REACHED_ERROR_MESSAGE = "Sorry, you reach the request limit, try again later... :("
API_CONNECTION_ERROR_MESSAGE = "I'm unable to connect with the server right now... :("
UNKNOWN_ARGS_ERROR_MESSAGE = "Please, use quotes in your first message"
QUIT_ARG_ERROR_MESSAGE = "Error: The -q/--quit flag requires a message."
EXIT_WORDS = [
    "q", "quit", "exit", "goodbye", "bye", "bye!", "gotta go", "byeee", "byebye", "goodbye!", "cya", "see ya",
    "later", "farewell", "adieu", "peace", "take care", "so long", "toodles",
    "catch you later", "hasta la vista", "sayonara", "au revoir"
]