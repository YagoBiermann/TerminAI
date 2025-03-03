import argparse
import re
import sys
from colorama import Fore
from api import call_ai, connect_to_openAI
import api
from arguments import parse_arguments
from commands import ConfirmCommand, RunCommand
from constants import AI_NAME, CHAT_HISTORY, EXIT_WORDS, PERSONA, QUIT_ARG_ERROR_MESSAGE
from display_messages import display_ai_response, display_powershell_command
from spinner import Spinner

class ChatExitException(Exception):
  pass

def init_chat():
  args = parse_arguments()
  api.OpenAIClient = connect_to_openAI()
  handle_invalid_args(args)
  with_message_and_quit(args)
  with_message(args)
  without_message(args)

def handle_invalid_args(args: argparse.Namespace):
  if args.message is None and args.quit:
    print(QUIT_ARG_ERROR_MESSAGE)
    sys.exit(1)

def with_message_and_quit(args: argparse.Namespace):
  if args.message and args.quit:
    handle_user_interaction(CHAT_HISTORY, args.message)
    sys.exit(0)

def with_message(args: argparse.Namespace):
  if args.message and not args.quit:
    handle_user_interaction(CHAT_HISTORY, args.message)
    chat_loop(CHAT_HISTORY)

def without_message(args: argparse.Namespace):
  if not args.message:
    handle_user_interaction(CHAT_HISTORY, f"Hi {AI_NAME}!")
    chat_loop(CHAT_HISTORY)

def chat_loop(chat_history: list) -> None:
  while True:
    try:
      trim_chat_history(chat_history)
      user_message = get_user_input()
      if not user_message:
        continue
      if match_exit_pattern(user_message, chat_history):
        break
      handle_user_interaction(chat_history, user_message)
    except ChatExitException:
      break

def trim_chat_history(chat_history: list):
    if len(chat_history) > 20:
      chat_history[:] = chat_history[-10:]
      chat_history.insert(0, PERSONA)

def get_user_input() -> str:
  try:
    user_message = input(Fore.LIGHTGREEN_EX + "\n\nYou: " + Fore.RESET)
    return user_message
  except (KeyboardInterrupt, EOFError):
    raise ChatExitException()

def match_exit_pattern(user_message: str, chat_history: list) -> bool:
  exit_pattern = rf"\b({'|'.join(re.escape(word) for word in EXIT_WORDS)})(?:[\s,!.?:;]+{re.escape(AI_NAME)})?[\s!?.:;]*\b"
  match_exit_pattern = re.search(exit_pattern, user_message.lower(), re.IGNORECASE)
  if match_exit_pattern:
    handle_user_interaction(chat_history, user_message)
    return True

def handle_user_interaction(chat_history: list, user_message: str):
  with Spinner():
    chat_history.append({"role": "user", "content": user_message})
    api_response = call_ai(chat_history)
    
  chat_history.append({"role":"assistant", "content": api_response.response})
  display_ai_response(api_response.response)
  display_powershell_command(api_response.is_powershell_command, api_response.powershell_command)
  handle_powershell_command(api_response.is_powershell_command, api_response.powershell_command)

def handle_powershell_command(is_powershell_command: bool, command: str):
  if is_powershell_command:
    if ConfirmCommand():
      RunCommand(command)