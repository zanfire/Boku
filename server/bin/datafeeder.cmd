@echo off
SET DIR=%~dp0

SET MOSQDIR=%ProgramFiles(X86)%\mosquitto

REM start services.
pushd %MOSQDIR%
call "%MOSQDIR%\mosquitto.exe"

:begin
SET /a value=%RANDOM% %%10 +13
call "%MOSQDIR%\mosquitto_pub.exe" -h 127.0.0.1 -t "Telemetries/Room/Bedroom/TempC" -m %value%.0
echo send %value%
SET /a value=%RANDOM% %%10 +13
call "%MOSQDIR%\mosquitto_pub.exe" -h 127.0.0.1 -t "Telemetries/Room/AliceRoom/TempC" -m %value%.0
echo send %value%
SET /a value=%RANDOM% %%10 +13
call "%MOSQDIR%\mosquitto_pub.exe" -h 127.0.0.1 -t "Telemetries/Room/Aisle/TempC" -m %value%.0
echo send %value%
SET /a value=%RANDOM% %%10 +13
call "%MOSQDIR%\mosquitto_pub.exe" -h 127.0.0.1 -t "Telemetries/Room/DayRoom/TempC" -m %value%.0
echo send %value%


sleep 60
goto begin

popd
