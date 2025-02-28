import subprocess
import shlex

def ConfirmCommand() -> bool:
    while True:
        confirmAction = input("Run command? [Y/N]\n").strip().upper()
        if confirmAction == "Y":
            return True
        elif confirmAction == "N":
            return False
        
def RunCommand(command: str) -> None:
    try:
      split_command = ["powershell", "-Command"] + shlex.split(command)
      result = subprocess.run(split_command, capture_output=True, text=True)
      print(result.stdout)
    except subprocess.CalledProcessError:
        print("\nInvalid command!")
        return None