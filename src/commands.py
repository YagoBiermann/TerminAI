import subprocess
from src.display_messages import display_ai_response
from src.spinner import Spinner
from src.utils import clear_currentLine, clear_lines_above

EMPTY_OUTPUT_MESSAGE = "No output was returned"

def confirm_command() -> bool:
    while True:
      try:
        confirmAction = input("Run command? [Y/N]\n").strip().upper()
        clear_lines_above(2)
        return True if confirmAction == "Y" else False
      except (KeyboardInterrupt, EOFError):
        break 

def reconfirm_command():
   display_ai_response("Are you sure?")
   return confirm_command()

def run_command(command: str) -> None:
    with Spinner():
      try:
        split_command = ["powershell", "-Command", command]
        result = subprocess.run(split_command, capture_output=True, text=True)
        clear_currentLine()
        if not result.stdout.strip():
          print(EMPTY_OUTPUT_MESSAGE)
        else:
          print(result.stdout)
      except subprocess.CalledProcessError:
          print("\nInvalid command!")
          return None