@echo off
SET DIR=%~dp0

python -m pdb %DIR%..\bokuserver\main.py -d %DIR%datastore.db %*

pause
