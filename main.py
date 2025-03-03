#!/usr/bin/env python3
from dotenv import load_dotenv
from chat import init_chat

def main():
  load_dotenv()
  init_chat()

if __name__ == "__main__":
  main()