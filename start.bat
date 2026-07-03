@echo off
title Docker Compose Network Linker

:: 1. Start the docker containers
echo Starting Docker containers...
docker compose up -d

:: 2. Grab the local IP address (Wi-Fi or Ethernet)
for /f "tokens=*" %%i in ('powershell -Command "(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Wi-Fi','Ethernet' | Where-Object {$_.IPAddress -notlike '169.254.*'} | Select-Object -First 1).IPAddress"') do set IP=%%i

:: 3. Grab the dynamic port from Docker Compose
for /f "tokens=2 delims=:" %%i in ('docker compose port start-stream-asst 8080') do set PORT=%%i

:: 4. Strip any accidental spaces out of the port number
set PORT=%PORT: =%

:: 5. Output the final clickable link
echo.
echo Accessible on your network at: http://%IP%:%PORT%
echo.

pause
