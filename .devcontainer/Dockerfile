# .devcontainer/Dockerfile
# FROM python:3.11-slim
FROM mcr.microsoft.com/devcontainers/python:3.11

# Оновлюємо пакети та встановлюємо системні залежності для OpenCV
# libgl1 і libglib2.0-0 критично важливі для роботи cv2 в Linux
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Створюємо робочу директорію
WORKDIR /workspace

# Оновлюємо pip
RUN pip install --upgrade pip