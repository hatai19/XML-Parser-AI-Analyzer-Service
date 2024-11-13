FROM python:3.12-slim

WORKDIR /app

# Устанавливаем только FastAPI
RUN pip install fastapi uvicorn

# Копируем весь проект в рабочую директорию контейнера
COPY . .

# Указываем команду, которая будет выполняться при запуске контейнера
CMD ["python", "main.py"]