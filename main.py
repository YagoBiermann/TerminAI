#!/usr/bin/env python3

from openai import OpenAI
import sys
import argparse
from dotenv import load_dotenv
import os
import persona
import re
import time
import threading

PERSONA = {"role": "system", "content": persona.persona_description}
CHAT_HISTORY = [PERSONA]
AI_NAME = persona.selected_persona["name"]
DEFAULT_ERROR_MESSAGE = "Sorry, I can't answer now..."
EXIT_WORDS = [
    "q", "quit", "exit", "goodbye", "bye", "bye!", "goodbye!", "cya", "see ya",
    "later", "farewell", "adieu", "peace", "take care", "so long", "toodles",
    "catch you later", "hasta la vista", "sayonara", "au revoir"
]
exit_pattern = rf"\b({'|'.join(re.escape(word) for word in EXIT_WORDS)})(?:[\s,!.?:;]+{re.escape(AI_NAME)})?[\s!?.:;]*\b"

def spinner(stop_event: threading.Event):
    spinner_chars = ['-', '\\', '|', '/']
    while not stop_event.is_set():
        for symbol in spinner_chars:
            if stop_event.is_set():
              break
            sys.stdout.write(f"\r {symbol} ")
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write("\r" + " " * 20 + "\r")
    sys.stdout.flush()

def show_spinner():
  stop_event = threading.Event()
  spinner_thread = threading.Thread(target=spinner, args=(stop_event,))
  spinner_thread.start()

  return spinner_thread, stop_event

def stop_spinner(spinner_thread: threading.Thread, stop_event: threading.Event):
  stop_event.set()
  spinner_thread.join()

def handle_user_interaction(chat_history: list, user_message: str):
  try:
    chat_history.append({"role": "user", "content": user_message})
    spinner_thread, stop_event = show_spinner()
    response = call_ai(chat_history)
  except:
    display_ai_response(response)
  finally:
    stop_spinner(spinner_thread, stop_event)
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
    return "Sorry, I can't answer now..."
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
      user_message = input("\nYou: ")
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