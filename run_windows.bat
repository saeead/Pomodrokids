@echo off
setlocal

REM Always run source (not stale dist exe)
cd /d %~dp0

if not exist .venv (
  py -3.10 -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul
pip install -r requirements.txt
python main.py
