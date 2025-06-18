# Базовый образ Python
FROM python:3.10-slim

# Рабочая директория
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Порт для FastAPI
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "src.api.rest_api:app", "--host", "0.0.0.0", "--port", "8000"]