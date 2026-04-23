@echo off
setlocal enabledelayedexpansion
title ShaneBrain // MASTER BLASTER LAUNCHER
color 0E

echo.
echo  ============================================================
echo       SHANEBRAIN MASTER BLASTER LAUNCHER v1.0
echo  ============================================================
echo.
echo   Starting entire three-node cluster + all services...
echo.

set SHANEBRAIN_ROOT=D:\Angel_Cloud\shanebrain-core

REM ============================================================
REM PREFLIGHT: RAM CHECK
REM ============================================================
echo  [PREFLIGHT] Checking available RAM...
for /f "tokens=2 delims==" %%A in ('wmic OS get FreePhysicalMemory /value') do set FreeRAM=%%A
set /a FreeRAM_MB=%FreeRAM:~0,-3%

if %FreeRAM_MB% LSS 1500 (
    echo.
    echo  !WARNING: Only %FreeRAM_MB% MB free. Recommended: 1500+ MB
    echo  Close Chrome/Edge for better performance.
    echo.
    pause
)
echo  [OK] RAM: %FreeRAM_MB% MB free

REM ============================================================
REM NODE STATUS CHECK
REM ============================================================
echo.
echo  [PREFLIGHT] Checking cluster nodes...

REM Check Computer B
curl -s --connect-timeout 2 http://192.168.100.2:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo  [INFO] Computer B: OFFLINE
    set NODE_B=0
) else (
    echo  [OK] Computer B: ONLINE (192.168.100.2)
    set NODE_B=1
)

REM Check Raspberry Pi
curl -s --connect-timeout 2 http://10.0.0.42:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo  [INFO] Raspberry Pi: OFFLINE
    set NODE_PI=0
) else (
    echo  [OK] Raspberry Pi: ONLINE (10.0.0.42)
    set NODE_PI=1
)

set /a TOTAL_NODES=1+%NODE_B%+%NODE_PI%
echo.
echo  [INFO] Cluster mode: %TOTAL_NODES%/3 nodes detected

REM ============================================================
REM STEP 1: Start Ollama (Computer A - Primary)
REM ============================================================
echo.
echo  [1/6] Starting Ollama on Computer A (Primary)...
start "Ollama A (Primary)" cmd /c "set OLLAMA_HOST=0.0.0.0:11434 && set OLLAMA_ORIGINS=* && ollama serve"
echo        Waiting 10 seconds for Ollama...
ping -n 10 127.0.0.1 >nul

curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo  !ERROR: Ollama failed to start
    pause
    exit /b 1
) else (
    echo  [OK] Ollama A ready: http://192.168.100.1:11434
)

REM ============================================================
REM STEP 2: Docker Desktop
REM ============================================================
echo.
echo  [2/6] Starting Docker Desktop...
if not exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
    echo  !ERROR: Docker not found
    pause
    exit /b 1
)
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
echo        Waiting 45 seconds for Docker...
ping -n 45 127.0.0.1 >nul
echo  [OK] Docker started

REM ============================================================
REM STEP 3: Weaviate
REM ============================================================
echo.
echo  [3/6] Starting Weaviate...
cd /d "%SHANEBRAIN_ROOT%\weaviate-config"
docker-compose down >nul 2>&1
docker-compose up -d

if errorlevel 1 (
    echo  !ERROR: Weaviate failed
    pause
    exit /b 1
)

echo        Waiting 15 seconds for Weaviate...
ping -n 15 127.0.0.1 >nul

curl -s http://localhost:8080/v1/.well-known/ready >nul 2>&1
if errorlevel 1 (
    echo  !WARNING: Weaviate not ready yet
) else (
    echo  [OK] Weaviate ready: http://localhost:8080
)

REM ============================================================
REM STEP 4: Load Balancer (routes between A, B, Pi)
REM ============================================================
echo.
echo  [4/6] Starting Load Balancer...
if exist "%SHANEBRAIN_ROOT%\ollama_loadbalancer.py" (
    start "Load Balancer" cmd /c "cd /d %SHANEBRAIN_ROOT% && python ollama_loadbalancer.py"
    echo        Waiting 5 seconds for Load Balancer...
    ping -n 5 127.0.0.1 >nul
    
    curl -s http://localhost:8000/health >nul 2>&1
    if errorlevel 1 (
        echo  !WARNING: Load Balancer not ready
    ) else (
        echo  [OK] Load Balancer ready: http://localhost:8000/dashboard
    )
) else (
    echo  !ERROR: ollama_loadbalancer.py not found
    pause
    exit /b 1
)

REM ============================================================
REM STEP 5: Angel Arcade Bot (background)
REM ============================================================
echo.
echo  [5/6] Starting Angel Arcade bot...
if exist "%SHANEBRAIN_ROOT%\arcade\arcade_bot.py" (
    start "Angel Arcade" cmd /c "cd /d %SHANEBRAIN_ROOT%\arcade && python arcade_bot.py"
    echo  [OK] Angel Arcade starting in background
) else (
    echo  !WARNING: arcade_bot.py not found - skipping
)

REM ============================================================
REM STEP 6: ShaneBrain Discord Bot (foreground)
REM ============================================================
echo.
echo  [6/6] Starting ShaneBrain Discord Bot...
echo.
echo  ============================================================
echo       SHANEBRAIN CLUSTER ONLINE
echo  ============================================================
echo.
echo   Dashboard:     http://localhost:8000/dashboard
echo   Ollama A:      http://192.168.100.1:11434 [ONLINE]
if %NODE_B%==1 (
echo   Ollama B:      http://192.168.100.2:11434 [ONLINE]
) else (
echo   Ollama B:      http://192.168.100.2:11434 [OFFLINE]
)
if %NODE_PI%==1 (
echo   Raspberry Pi:  http://10.0.0.42:11434 [ONLINE]
) else (
echo   Raspberry Pi:  http://10.0.0.42:11434 [OFFLINE]
)
echo   Weaviate:      http://localhost:8080
echo   Arcade Bot:    Running in background
echo.
echo   Active Nodes:  %TOTAL_NODES%/3
echo.
echo  ============================================================
echo.

if not exist "%SHANEBRAIN_ROOT%\bot\bot.py" (
    echo  !ERROR: bot.py not found
    pause
    exit /b 1
)

cd /d "%SHANEBRAIN_ROOT%\bot"
set OLLAMA_HOST=http://localhost:8000

python bot.py

if errorlevel 1 (
    echo.
    echo  !ERROR: Bot crashed. Check logs above.
)
pause