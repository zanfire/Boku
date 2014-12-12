@echo off
SET DIR=%~dp0


python %DIR%..\bokuserver\main.py -d %DIR%datastore.db %*
