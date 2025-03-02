import subprocess
import shlex

def ConfirmCommand() -> bool:
    while True:
      try:
        confirmAction = input("Run command? [Y/N]\n").strip().upper()
        ClearLine()
        return True if confirmAction == "Y" else False
      except (KeyboardInterrupt, EOFError):
        break 
        
def RunCommand(command: str) -> None:
        ClearLine()
