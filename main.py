#!/usr/bin/env python3
from dotenv import load_dotenv
from src.chat import init_chat

if __name__ == "__main__":
  load_dotenv()
  init_chat()