from colorama import Fore
from src.constants import AI_NAME

def display_ai_response(message):
    try:
      print(f"\n{Fore.LIGHTBLUE_EX}{AI_NAME}{Fore.RESET}: " + message.format(Fore=Fore))
    except Exception as e:
      print(e)

def display_powershell_command(command:str | None):
  if command is None:
    return
  print(f"\n{Fore.LIGHTBLUE_EX}{AI_NAME}{Fore.RESET}: " + command)
