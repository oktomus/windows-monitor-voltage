
@echo off

if "%~1"=="" (
    echo Specify the python script to run as the first argument.
)

if not exist %~1 (
    echo %date% %time% Error - File %~1 doesn't exist.
    exit /b 1
)


echo %date% %time% Running python script %~1...
set "PYTHON_COMMAND=python "%~1""


start /B /WAIT "Run python script " %PYTHON_COMMAND%
if %ERRORLEVEL% NEQ 0 (
    echo %date% %time% python script failed.
    exit /b 1
)

endlocal