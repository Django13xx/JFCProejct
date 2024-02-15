@echo off

REM Get the current directory of the batch file
set "script_dir=%~dp0"

REM Clear previous output files
type nul > "%script_dir%..\aus\ausback\output_ausback.txt"
type nul > "%script_dir%..\aus\ausfront\output_ausfront.txt"
type nul > "%script_dir%..\Hardware\output_hardware.txt"

REM Run command in ausback directory
cd /d "%script_dir%..\aus\ausback"
start cmd /k "python manage.py runserver > %script_dir%..\aus\ausback\output_ausback.txt"

REM Run command in ausfront directory
cd /d "%script_dir%..\aus\ausfront"
start cmd /k "npm run dev > %script_dir%..\aus\ausfront\output_ausfront.txt"

REM Run command in Hardware directory
cd /d "%script_dir%..\Hardware"
start cmd /k "node app.js > %script_dir%..\Hardware\output_hardware.txt"

REM Wait for python manage.py runserver to finish loading
:WAIT_LOOP_AUSBACK
findstr /C:"Starting development server at http://127.0.0.1:8000/" "%script_dir%..\aus\ausback\output_ausback.txt" > nul
if errorlevel 1 (
    goto :WAIT_LOOP_AUSBACK
)

REM Wait for npm run dev to finish loading
:WAIT_LOOP_AUSFRONT
:: Use PowerShell to read file content and check for the specific string
powershell -Command "& { $content = Get-Content '%script_dir%..\aus\ausfront\output_ausfront.txt' -Raw; if ($content -match 'ausfront@0.0.0 dev') { exit 0 } else { exit 1 } }"
if errorlevel 1 (
    goto :WAIT_LOOP_AUSFRONT
)

REM Clear output files
type nul > "%script_dir%..\aus\ausback\output_ausback.txt"
type nul > "%script_dir%..\aus\ausfront\output_ausfront.txt"
type nul > "%script_dir%..\Hardware\output_hardware.txt"


REM Wait for 1 second before opening the specified URL
timeout /t 1


REM Open the specified URL in the default browser
start http://localhost:5173/