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
    with Spinner():
        ClearLine()
        if not result.stdout.strip():
          print(EMPTY_OUTPUT_MESSAGE)
        else:
          print(result.stdout)
