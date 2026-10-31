FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ .

# Создаем папку для данных на случай, если volume не примонтировался
RUN mkdir -p /data

# Указываем путь к базе данных в постоянном хранилище
ENV DATABASE_URL=sqlite+aiosqlite:////data/bot.db

CMD ["python", "main.py"]