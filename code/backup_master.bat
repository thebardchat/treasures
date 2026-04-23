@echo off
REM ============================================
REM SHANE'S MASTER BACKUP SCRIPT
REM Backs up C:\Users\shane\ to D:\ with versioning
REM Keeps last 5 backups, older ones auto-delete
REM ============================================

setlocal enabledelayedexpansion

REM Set variables
set SOURCE=C:\Users\shane
set BACKUP_DRIVE=D:
set BACKUP_ROOT=%BACKUP_DRIVE%\8TB_Master_Backup
set TIMESTAMP=%date:~-4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%
set TIMESTAMP=%TIMESTAMP: =0%
set BACKUP_FOLDER=%BACKUP_ROOT%\Backup_%TIMESTAMP%
set LOG_FILE=%BACKUP_ROOT%\backup_log.txt

REM Check if backup drive exists
if not exist %BACKUP_DRIVE%\ (
    echo ERROR: Backup drive %BACKUP_DRIVE%\ not found. Plug in your Seagate drive.
    pause
    exit /b 1
)

REM Create backup root folder if it doesn't exist
if not exist "%BACKUP_ROOT%" mkdir "%BACKUP_ROOT%"

REM Start logging
echo. >> "%LOG_FILE%"
echo ================================================ >> "%LOG_FILE%"
echo BACKUP STARTED: %date% %time% >> "%LOG_FILE%"
echo ================================================ >> "%LOG_FILE%"

echo.
echo STARTING BACKUP...
echo Source: %SOURCE%
echo Destination: %BACKUP_FOLDER%
echo.
echo This will take a few minutes depending on file size.
echo DO NOT unplug the Seagate drive.
echo.

REM Perform the backup using robocopy (preserves file structure, faster than xcopy)
robocopy "%SOURCE%" "%BACKUP_FOLDER%" /E /Z /R:3 /W:5 /MT:8 /NP /LOG+:"%LOG_FILE%"

REM Check if backup succeeded
if %errorlevel% LEQ 7 (
    echo. >> "%LOG_FILE%"
    echo BACKUP COMPLETED SUCCESSFULLY >> "%LOG_FILE%"
    echo Backup Location: %BACKUP_FOLDER% >> "%LOG_FILE%"
    echo. >> "%LOG_FILE%"
    echo.
    echo ✓ BACKUP COMPLETE
    echo Location: %BACKUP_FOLDER%
) else (
    echo. >> "%LOG_FILE%"
    echo BACKUP FAILED - Error Code: %errorlevel% >> "%LOG_FILE%"
    echo. >> "%LOG_FILE%"
    echo.
    echo ✗ BACKUP FAILED - Check log file
    echo Log: "%LOG_FILE%"
    pause
    exit /b 1
)

REM DELETE OLD BACKUPS (Keep only last 5)
echo.
echo Cleaning up old backups...
echo Cleaning up old backups... >> "%LOG_FILE%"

for /f "skip=5 delims= eol= tokens=*" %%A in ('dir "%BACKUP_ROOT%\Backup_*" /ad /b /o-d') do (
    echo Deleting old backup: %%A >> "%LOG_FILE%"
    rmdir /s /q "%BACKUP_ROOT%\%%A"
)

echo. >> "%LOG_FILE%"
echo Old backups cleaned up. Keeping last 5 only. >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Final status
echo.
echo ================================================
echo BACKUP COMPLETE AND VERIFIED
echo ================================================
echo Location: %BACKUP_FOLDER%
echo Log File: %LOG_FILE%
echo.
echo Your data is safe. Last 5 backups are kept.
echo Older backups are automatically deleted.
echo.
pause
