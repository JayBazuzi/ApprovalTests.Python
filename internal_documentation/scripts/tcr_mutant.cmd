@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0..\.."

set "MUTMUT=.venv\Scripts\mutmut.exe"
set "PYTHON=.venv\Scripts\python.exe"

if not exist .ignore\mutant_id.txt (
    %PYTHON% -m pytest -q >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo build working
        exit /b 0
    )
    echo build broken
    exit /b 1
)

git checkout -- approvaltests approval_utilities

%PYTHON% -m pytest -q >nul 2>&1
if not !ERRORLEVEL! EQU 0 (
    git checkout -- .
    git clean -fd
    echo tcr: reverted ^(test suite is failing^)
    exit /b 1
)

set /p MUTANT_ID=<.ignore\mutant_id.txt

%MUTMUT% run !MUTANT_ID! >nul 2>&1
if not !ERRORLEVEL! EQU 0 (
    git checkout -- .
    git clean -fd
    echo tcr: reverted ^(mutant #!MUTANT_ID! still survives^)
    exit /b 1
)

if not exist .ignore\commit-message.txt >.ignore\commit-message.txt echo test: kill surviving mutant #!MUTANT_ID!

git add -A
git commit -F .ignore\commit-message.txt >nul
echo tcr: committed ^(mutant #!MUTANT_ID! killed^)
exit /b 0
