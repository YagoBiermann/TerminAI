import sys

def ClearLinesAbove(n: int = 1):
    for _ in range(n):
        sys.stdout.write("\033[F")  # Move cursor up
        sys.stdout.write("\r\033[K")  # Clear the line
    sys.stdout.flush()