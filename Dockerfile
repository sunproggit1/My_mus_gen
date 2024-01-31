# Базовый образ
FROM python:latest
# Установка рабочей директории в контейнере
WORKDIR /midi

# Установка nano и обновление pip
RUN apt-get update && apt-get install -y nano && \
    pip install --upgrade pip

# Копирование файла зависимостей и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта в контейнер
COPY . .

# Сбор статических файлов
RUN python manage.py collectstatic --noinput

# Открытие порта 8000
EXPOSE 8000


CMD python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000
# CMD ["/bin/sh","-c","entrypoint.sh"]


