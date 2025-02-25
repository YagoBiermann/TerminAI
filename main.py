#!/usr/bin/env python3

from openai import OpenAI
import sys
import argparse
from dotenv import load_dotenv
import os
import persona

INITIAL_MESSAGES = [{"role": "system", "content": persona.persona_description}]

def call_AI(messages):
  client = OpenAI(api_key=os.getenv("API_KEY"))
  
  response = client.chat.completions.create(
      model=os.getenv("MODEL"),
      store=False,
      messages = messages,
      temperature=float(os.getenv("TEMPERATURE")),
      stream=False
  )  
  return response.choices[0].message.content

def assistant_response(message):
    print(f"\n{persona.selected_persona["name"]}: {message}")

def chat(messages, message=None, quit_after_response=False):
  if message:
    new_messages = messages + [{"role": "user", "content": message}]
    response = call_AI(new_messages)
    assistant_response(response)
  if quit_after_response:
    sys.exit(0)

  else:
    new_messages = messages
  
  while True:
    if len(new_messages) > 20:
      new_messages = new_messages[-10:]
    
    user_message = input("\nYou: ")
    if not user_message:
      continue

    if user_message.lower() == "q":
      assistant_response("See you next time! :)")
      break
    
    new_messages = messages + [{"role": "user", "content": user_message}]
    response = call_AI(new_messages)
    new_messages = new_messages + [{"role": "assistant", "content": response}]

    assistant_response(response)

def parse_arguments():
  parser = argparse.ArgumentParser(description="Inline AI assistance")
  parser.add_argument("message", nargs="?", type=str, default=None, help="Ask anything")
  parser.add_argument("-q", "--quit", action="store_true", help="Quit after the first response", required=False)
  args, unknown_args = parser.parse_known_args()
  if unknown_args:
    print(f"Please, use quotes in your first message")
    exit(1)

  return args


if __name__ == "__main__":
  load_dotenv()
  args = parse_arguments()

  if args.message is None and args.quit:
    print("Error: The -q/--quit flag requires a message.")
    sys.exit(1)

  if args.message:
    chat(INITIAL_MESSAGES,args.message, args.quit)
  else:
    print("How can I help you today?")
    chat(INITIAL_MESSAGES)