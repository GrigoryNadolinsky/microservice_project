# Этап 1: Сборка
FROM python:3.11-slim AS builder

WORKDIR /app

# Копируем файл с зависимостями
COPY app/requirements.txt requirements.txt

# Устанавливаем зависимости в виртуальную среду
RUN python -m venv /venv && /venv/bin/pip install -r requirements.txt

# Копируем всё приложение
COPY app/ .

# Этап 2: Финальный образ
FROM python:3.11-slim

WORKDIR /app

# Копируем виртуальную среду из этапа сборки
COPY --from=builder /venv /venv

# Копируем приложение из этапа сборки
COPY --from=builder /app .

# Устанавливаем переменную окружения для использования виртуальной среды
ENV PATH="/venv/bin:$PATH"

# Запускаем приложение
CMD ["python", "app.py"]
