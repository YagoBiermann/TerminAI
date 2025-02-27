import sys
import threading
import time


class Spinner:
  spinner_chars = ['-', '\\', '|', '/']

  def __init__(self, delay: float = 0.1):
    self.delay = delay
    self.stop_event = threading.Event()
    self.thread = threading.Thread(target=self._spin)
  
  def _spin(self):
    while not self.stop_event.is_set():
      for symbol in self.spinner_chars:
        if self.stop_event.is_set():
          break
        sys.stdout.write(f"\r {symbol} ")
        sys.stdout.flush()
        time.sleep(self.delay)
    sys.stdout.write("\r" + " " * 20 + "\r")
    sys.stdout.flush()

  def __enter__(self):
    self.thread.start()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.stop_event.set()
    self.thread.join()
    sys.stdout.write("\r" + " " * 20 + "\r")
    sys.stdout.flush()
