# Локальний помічник програміста
Windows, Python 3.10+, Ollama. Tkinter входить до стандартного дистрибутива Python для Windows.

```bash
ollama pull qwen3:4b
python app.py
```
API: http://localhost:11434/v1/chat/completions. Температура 0.2, максимум 512 токенів, reasoning_effort none; контекст визначає Ollama (у вимірюванні 4096). Введіть запит і натисніть «Отримати відповідь». Для benchmark та quality_test потрібен пакет openai (`python -m pip install openai`).
