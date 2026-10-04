FROM python:3.10-slim

WORKDIR /app

# Добавляем wget и unzip для скачивания Allure
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    firefox-esr \
    gcc \
    wget \
    unzip \
    default-jre \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Allure
RUN wget -q -O allure.zip https://github.com/allure-framework/allure2/releases/download/2.30.0/allure-2.30.0.zip \
    && unzip allure.zip -d /opt/ \
    && rm allure.zip \
    && ln -s /opt/allure-2.30.0/bin/allure /usr/local/bin/allure \
    && chmod +x /usr/local/bin/allure

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ВСЕ файлы проекта
COPY . .

WORKDIR /app/src

ENTRYPOINT ["pytest"]
CMD []
ENV PYTHONPATH=/app/src