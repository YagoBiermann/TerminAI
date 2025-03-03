from colorama import Fore
from constants import AI_NAME

def display_ai_response(message):
    try:
      print(f"\n{Fore.LIGHTBLUE_EX}{AI_NAME}{Fore.RESET}: " + message.format(Fore=Fore))
    except Exception as e:
      print(e)

def display_powershell_command( is_powershell_command: bool, command:str):
  if is_powershell_command:
    print(f"\n{Fore.LIGHTBLUE_EX}{AI_NAME}{Fore.RESET}: " + command)
