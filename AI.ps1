$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

python "$scriptPath\main.py" $args