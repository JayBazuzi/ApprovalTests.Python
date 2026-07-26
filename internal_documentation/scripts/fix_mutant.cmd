@echo off
setlocal
cd /d "%~dp0..\.."

type .\internal_documentation\mutation.process.md | claude --dangerously-skip-permissions -p --output-format text --verbose
