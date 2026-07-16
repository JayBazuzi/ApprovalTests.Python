@echo off
setlocal

set COUNT_FILE=..\..\.ignore\mutation_count.txt

if not exist "%COUNT_FILE%" (
    echo 0 > "%COUNT_FILE%"
)

set /p count= < "%COUNT_FILE%"

if %count% == 2 (
    echo Test passed on mutated code; expected it to fail. >&2
    exit /b 1
)

exit /b 0
