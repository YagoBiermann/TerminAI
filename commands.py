import subprocess
import shlex

def ConfirmCommand() -> bool:
    while True:
      try:
        confirmAction = input("Run command? [Y/N]\n").strip().upper()
        sys.stdout.flush()
        return True if confirmAction == "Y" else False
      except (KeyboardInterrupt, EOFError):
        break 
        
def RunCommand(command: str) -> None:
    try:
      split_command = ["powershell", "-Command"] + shlex.split(command)
      result = subprocess.run(split_command, capture_output=True, text=True)
      print(result.stdout)
    except subprocess.CalledProcessError:
        print("\nInvalid command!")
        return None