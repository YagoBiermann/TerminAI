import sys
import ctypes

def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

def clear_currentLine():
  sys.stdout.write("\r\033[K")
  sys.stdout.flush()

def clear_lines_above(n: int = 1):
    for _ in range(n):
        sys.stdout.write("\033[F")  # Move cursor up
        sys.stdout.write("\r\033[K")  # Clear the line
    sys.stdout.flush()