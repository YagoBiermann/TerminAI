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

def handle_user_interaction(chat_history: list, user_message: str):
  chat_history.append({"role": "user", "content": user_message})
  response = call_ai(chat_history)
  chat_history.append({"role":"assistant", "content": response})
  display_ai_response(response)

def call_ai(messages: list) -> str:
  client = OpenAI(api_key=os.getenv("API_KEY"))

  stop_event = threading.Event()
  spinner_thread = threading.Thread(target=spinner, args=(stop_event,))
  spinner_thread.start()

  try:
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        store=False,
        messages = messages,
        temperature=float(os.getenv("TEMPERATURE")),
        stream=False
    )
    ai_response = response.choices[0].message.content
  except: 
    return "Sorry, I can't answer now..."
  finally:
    stop_event.set()
    spinner_thread.join()

  return ai_response

def display_ai_response(message):
    print(f"\n{AI_NAME}: {message}")

def chat_loop(chat_history: list) -> None:
  while True:
    if len(chat_history) > 20:
      chat_history[-10:]
      chat_history.insert(0, PERSONA)
    
    try:
      user_message = input("\nYou: ")
    except (KeyboardInterrupt, EOFError):
      break

    if not user_message:
      continue

    if re.search(exit_pattern, user_message.lower(), re.IGNORECASE):
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
    exit(1)

  return args

def main():
  load_dotenv()
  args = parse_arguments()
  if args.message is None and args.quit:
    print("Error: The -q/--quit flag requires a message.")
    sys.exit(1)

  if args.message:
    handle_user_interaction(CHAT_HISTORY, args.message)
    chat_loop(CHAT_HISTORY)
    if args.quit:
      sys.exit(0)
  else:
    handle_user_interaction(CHAT_HISTORY, f"Hi {AI_NAME}!")
    chat_loop(CHAT_HISTORY)

if __name__ == "__main__":
  main()