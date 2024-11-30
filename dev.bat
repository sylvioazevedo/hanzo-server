@echo off
call venv\Scripts\activate
uv run -m flask --app flaskr run --debug --port 35777