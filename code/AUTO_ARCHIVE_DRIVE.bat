@echo off
set "SourceFolder=C:\Users\shane\Downloads\data-2025-10-05-21-09-36-batch-0000"
set "DestinationFolder=C:\Users\shane\Google Drive\Shanebrain_Code_Archive"

echo.
echo Starting secure copy for all Angel Cloud Assets...
echo.

REM Create the destination directory if it doesn't exist
if not exist "%DestinationFolder%" (
    mkdir "%DestinationFolder%"
    echo Created cloud archive folder: "%DestinationFolder%"
    echo.
)

REM The xcopy command will copy all files and folders efficiently.
xcopy "%SourceFolder%" "%DestinationFolder%\" /E /I /H /C /Y

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! All project files are now copying to Google Drive.
    echo You can find them in the folder named: "Shanebrain_Code_Archive"
    echo.
) else (
    echo.
    echo ERROR: Copy process failed. Please check your Google Drive path.
    echo.
)

pause