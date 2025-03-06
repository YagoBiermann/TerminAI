import persona
import rules
from utils import is_admin

RUNNING_WITH_PRIVILEGE = is_admin()
IS_ADMIN = f"\nIS ADMIN: {RUNNING_WITH_PRIVILEGE}\n\n"
AI_NAME = persona.selected_persona["name"]
PERSONA = {"role": "system", "content": IS_ADMIN + persona.persona_description + rules.rules}
CHAT_HISTORY = [PERSONA]
DEFAULT_ERROR_MESSAGE = "Sorry, I can't answer now..."
LIMIT_REACHED_ERROR_MESSAGE = "Sorry, you reach the request limit, try again later... :("
API_CONNECTION_ERROR_MESSAGE = "I'm unable to connect with the server right now... :("
UNKNOWN_ARGS_ERROR_MESSAGE = "Please, use quotes in your first message"
QUIT_ARG_ERROR_MESSAGE = "Error: The -q/--quit flag requires a message."