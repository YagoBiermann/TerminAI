import subprocess
from src.display_messages import display_ai_response
from src.spinner import Spinner
from src.utils import clear_currentLine, clear_lines_above
from colorama import Fore

EMPTY_OUTPUT_MESSAGE = "No output was returned"

def confirm_command() -> bool:
    while True:
      try:
        confirmAction = input(f"{Fore.LIGHTBLUE_EX}Run command?{Fore.RESET} [Y/N]\n").strip().upper()
        clear_lines_above(2)
        return True if confirmAction == "Y" else False
      except (KeyboardInterrupt, EOFError):
        break 

def reconfirm_command():
   display_ai_response(f"{Fore.LIGHTRED_EX}Are you sure?{Fore.RESET}")
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