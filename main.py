#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
from src.chat import init_chat

if __name__ == "__main__":
  load_dotenv()
  sys.path.append(os.path.abspath("src"))
  init_chat()