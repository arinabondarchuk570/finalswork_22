FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google.gpg \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

RUN pip install webdriver-manager

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pages/ ./pages/
COPY test_data/ ./test_data/
COPY tests/ ./tests/
COPY config.py .
COPY conftest.py .
COPY pytest.ini .

ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99
ENV WEB_DRIVER_WAIT=10
ENV DOCKER_ENV=true

ENV BASE_URL=http://host.docker.internal:3000

CMD ["pytest", "-v", "--tb=short"]
