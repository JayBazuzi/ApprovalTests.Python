@echo off
setlocal

set COUNT_FILE=..\..\.ignore\mutation_count.txt

if not exist "..\..\.ignore" mkdir "..\..\.ignore"

if not exist "%COUNT_FILE%" (
    echo 0 > "%COUNT_FILE%"
)

set /p count= < "%COUNT_FILE%"
if %count% GTR 3 set count=0
set /a count+=1
echo %count% > "%COUNT_FILE%"

if %count% LEQ 3 exit /b 0

echo 0 > "%COUNT_FILE%"
echo No surviving mutants found. >&2
exit /b 1
