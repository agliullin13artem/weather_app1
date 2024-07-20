# Используем официальный образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /usr/src/app

# Копируем файлы
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Выполняем миграции и запускаем сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
