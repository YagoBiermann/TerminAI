#!/usr/bin/env python3
from typing import Optional
from pydantic import BaseModel
import openai
from openai import OpenAI
import sys
import argparse
from dotenv import load_dotenv
import os
import persona
import re
from spinner import Spinner
from colorama import Fore, Style
from commands import ConfirmCommand, RunCommand

PERSONA = {"role": "system", "content": persona.persona_description}
CHAT_HISTORY = [PERSONA]
AI_NAME = persona.selected_persona["name"]
DEFAULT_ERROR_MESSAGE = "Sorry, I can't answer now..."
LIMIT_REACHED_ERROR_MESSAGE = "Sorry, you reach the request limit, try again later... :("
API_CONNECTION_ERROR_MESSAGE = "I'm unable to connect with the server right now... :("
UNKNOWN_ARGS_ERROR_MESSAGE = "Please, use quotes in your first message"
QUIT_ARG_ERROR_MESSAGE = "Error: The -q/--quit flag requires a message."

EXIT_WORDS = [
    "q", "quit", "exit", "goodbye", "bye", "bye!", "gotta go", "byeee", "goodbye!", "cya", "see ya",
    "later", "farewell", "adieu", "peace", "take care", "so long", "toodles",
    "catch you later", "hasta la vista", "sayonara", "au revoir"
]
exit_pattern = rf"\b({'|'.join(re.escape(word) for word in EXIT_WORDS)})(?:[\s,!.?:;]+{re.escape(AI_NAME)})?[\s!?.:;]*\b"

class AIResponse(BaseModel):
  is_powershell_command: bool
  powershell_command: Optional[str] = None
  response: str

def handle_user_interaction(chat_history: list, user_message: str):
  with Spinner():
    chat_history.append({"role": "user", "content": user_message})
    api_response = call_ai(chat_history)
    
  chat_history.append({"role":"assistant", "content": api_response.response})
  display_ai_response(api_response.response, api_response.is_powershell_command, api_response.powershell_command)
  
  if api_response.is_powershell_command:
    if ConfirmCommand():
      RunCommand(api_response.powershell_command)

def call_ai(messages: list):
  try:
    response = OpenAIClient.beta.chat.completions.parse(
        model=os.getenv("MODEL"),
        store=False,
        messages = messages,
        temperature=float(os.getenv("TEMPERATURE")),
        max_tokens=250,
        response_format=AIResponse
    )
    ai_response = response.choices[0].message.parsed
    return ai_response
  except openai.APIConnectionError as e:
    display_ai_response(API_CONNECTION_ERROR_MESSAGE)
    sys.exit(1)
  except openai.RateLimitError as e:
    display_ai_response(LIMIT_REACHED_ERROR_MESSAGE)
    sys.exit(1)
  except Exception as e:
    display_ai_response(DEFAULT_ERROR_MESSAGE)
    sys.exit(1)


def display_ai_response(message, is_powershell_command=False, powershell_command = None):
    try:
      print(f"\n{Fore.LIGHTBLUE_EX}{AI_NAME}{Fore.RESET}: " + message.format(Fore=Fore))
      if is_powershell_command:
        print(f"\n{Fore.LIGHTBLUE_EX}{AI_NAME}{Fore.RESET}: " + powershell_command)
    except Exception as e:
      print(e)


def trim_chat_history(chat_history: list):
    if len(chat_history) > 20:
      chat_history[:] = chat_history[-10:]
      chat_history.insert(0, PERSONA)

def chat_loop(chat_history: list) -> None:
  while True:
    trim_chat_history(chat_history)
    try:
      user_message = input(Fore.LIGHTGREEN_EX + "\n\nYou: " + Fore.RESET)
    except (KeyboardInterrupt, EOFError):
      break

    if not user_message:
      continue

    match_exit_pattern = re.search(exit_pattern, user_message.lower(), re.IGNORECASE)
    if match_exit_pattern:
      handle_user_interaction(chat_history, user_message)
      break

    handle_user_interaction(chat_history, user_message)

def parse_arguments():
  parser = argparse.ArgumentParser(description="Inline AI assistance")
  parser.add_argument("message", nargs="?", type=str, default=None, help="Ask anything")
  parser.add_argument("-q", "--quit", action="store_true", help="Quit after the first response", required=False)
  args, unknown_args = parser.parse_known_args()
  if unknown_args:
    print(UNKNOWN_ARGS_ERROR_MESSAGE)
    sys.exit(1)

  return args

def main():
  global OpenAIClient
  try:
    OpenAIClient = OpenAI(api_key=os.getenv("API_KEY"))
  except OpenAI.APIConnectionError:
    print("Unable to connect to OpenAI")

  load_dotenv()
  args = parse_arguments()
  if args.message is None and args.quit:
    print(QUIT_ARG_ERROR_MESSAGE)
    sys.exit(1)

  if args.message:
    handle_user_interaction(CHAT_HISTORY, args.message)
    if not args.quit:
      chat_loop(CHAT_HISTORY)
  else:
    handle_user_interaction(CHAT_HISTORY, f"Hi {AI_NAME}!")
    chat_loop(CHAT_HISTORY)

if __name__ == "__main__":
  main()