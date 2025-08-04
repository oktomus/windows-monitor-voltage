
@echo off
setlocal

:: Add dependencies to the PYTHONPATH
set "DEPS_PATH=%~dp0dependencies"
set "PYTHONPATH=%PYTHONPATH%;%DEPS_PATH%"

call "%~dp0Run_Python_Script.bat" %~dp0monitor_voltage.py

endlocal