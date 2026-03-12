# Использование образа системы с Python 3.12.2 уменьшенной версии slim.
FROM python:3.12.2-slim

# Устанавливаем системные зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*


# Установка /app как рабочей директории для команд Dockerfile, которые следуют далее.
WORKDIR /app


# Копируем только requirements (для кэширования)
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt


# Копирование всей текущей директории в /app в контейнере.
COPY . /app/


# Команда по умолчанию при запуске контейнера
CMD ["pytest", "-v"]
