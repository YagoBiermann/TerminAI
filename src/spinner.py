import sys
import threading
import time
from src.utils import clear_currentLine

class Spinner():
    def __init__(self):
        self.spinner_active = False
        self.spinner_thread = None

    def start(self):
      self.spinner_active = True
      self.spinner_thread = threading.Thread(target=self._spinner)
      self.spinner_thread.daemon = True
      self.spinner_thread.start()

    def _spinner(self):
      spinner_chars = "|/-\\"
      i = 0
      while self.spinner_active:
          sys.stdout.write(f"\r{spinner_chars[i % len(spinner_chars)]}")
          sys.stdout.flush()
          time.sleep(0.1)
          i += 1

    def stop(self):
      self.spinner_active = False
      if self.spinner_thread:
          self.spinner_thread.join()
      clear_currentLine()

    def __enter__(self) -> None:
      self.start()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
      self.stop()