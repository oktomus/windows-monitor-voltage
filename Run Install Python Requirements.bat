
@echo off
setlocal

:: Get path to requirements.txt
set "REQUIREMENTS_PATH=%~dp0requirements.txt"
:: Get path to the dependencies folder
set "DEPS_PATH=%~dp0dependencies"

set "PYTHON_COMMAND=python -m pip install -r "%REQUIREMENTS_PATH%" --target "%DEPS_PATH%""

start /B /WAIT "Install requirements" %PYTHON_COMMAND%
if %ERRORLEVEL% NEQ 0 (
    echo %date% %time% Error - Install requirements failed.
    exit /b 1
)

endlocal