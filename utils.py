import sys

def ClearLine():
  sys.stdout.write("\033[F")  # Move cursor up
  sys.stdout.write("\033[K")  # Clear the line
  sys.stdout.flush()