$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

python "$scriptPath\src\main.py" $args