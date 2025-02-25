# This script automates adding the current directory to the system PATH in Windows environment variables.
# This step is optional but makes it easier to run the AI from any location in the terminal.

# Example: Running without adding the folder to PATH:
# python "C:/path/to/terminAI/main.py" "your message"

# Example: Running after adding the folder to PATH:
# ai "your message"

$path = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::User)
$currentPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$newPath = "$path;$currentPath"
[System.Environment]::SetEnvironmentVariable("Path", $newPath, [System.EnvironmentVariableTarget]::User)