#!/usr/bin/env python3

from openai import OpenAI
import sys
import argparse
from dotenv import load_dotenv
import os
import persona
import re
from spinner import Spinner
from colorama import Fore, Back, Style

PERSONA = {"role": "system", "content": persona.persona_description}
CHAT_HISTORY = [PERSONA]
AI_NAME = persona.selected_persona["name"]
DEFAULT_ERROR_MESSAGE = "Sorry, I can't answer now..."
EXIT_WORDS = [
    "q", "quit", "exit", "goodbye", "bye", "bye!", "gotta go", "byeee", "goodbye!", "cya", "see ya",
    "later", "farewell", "adieu", "peace", "take care", "so long", "toodles",
    "catch you later", "hasta la vista", "sayonara", "au revoir"
]
exit_pattern = rf"\b({'|'.join(re.escape(word) for word in EXIT_WORDS)})(?:[\s,!.?:;]+{re.escape(AI_NAME)})?[\s!?.:;]*\b"

def handle_user_interaction(chat_history: list, user_message: str):
  with Spinner():
    try:
      chat_history.append({"role": "user", "content": user_message})
      response = call_ai(chat_history)
    except Exception as e:
      display_ai_response(DEFAULT_ERROR_MESSAGE)
      sys.exit(1)
    
  chat_history.append({"role":"assistant", "content": response})
  display_ai_response(response)

def call_ai(messages: list) -> str:
  try:
    response = OpenAIClient.chat.completions.create(
        model=os.getenv("MODEL"),
        store=False,
        messages = messages,
        temperature=float(os.getenv("TEMPERATURE")),
        stream=False
    )
    ai_response = response.choices[0].message.content
  except: 
    return DEFAULT_ERROR_MESSAGE
  return ai_response

def display_ai_response(message):
    print(f"\n{AI_NAME}: {message}")

def trim_chat_history(chat_history: list):
    if len(chat_history) > 20:
      chat_history[:] = chat_history[-10:]
      chat_history.insert(0, PERSONA)

def chat_loop(chat_history: list) -> None:
  while True:
    trim_chat_history(chat_history)
    try:
      user_message = input(Fore.LIGHTGREEN_EX + "\nYou: " + Style.RESET_ALL)
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
    print(f"Please, use quotes in your first message")
    sys.exit(1)

  return args

def main():
  global OpenAIClient
  try:
    OpenAIClient = OpenAI(api_key=os.getenv("API_KEY"))
  except:
    print("Unable to connect to OpenAI")

  load_dotenv()
  args = parse_arguments()
  if args.message is None and args.quit:
    print("Error: The -q/--quit flag requires a message.")
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