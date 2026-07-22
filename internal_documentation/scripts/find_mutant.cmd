@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0..\.."

set "MUTMUT=.venv\Scripts\mutmut.exe"

if not exist .ignore mkdir .ignore

%MUTMUT% run >nul 2>&1

set "SURVIVORS="
for /f "usebackq delims=" %%i in (`%MUTMUT% result-ids survived 2^>nul`) do set "SURVIVORS=%%i"

if "!SURVIVORS!"=="" (
    echo no surviving mutants
    exit /b 1
)

for /f "tokens=1 delims= " %%a in ("!SURVIVORS!") do set "MUTANT_ID=%%a"

>.ignore\mutant_id.txt echo(!MUTANT_ID!
%MUTMUT% show !MUTANT_ID! >.ignore\mutant.txt

echo surviving mutant #!MUTANT_ID!
type .ignore\mutant.txt
exit /b 0
