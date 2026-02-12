FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# System-Abhängigkeiten für Musik-Bots
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    g++ \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Sicherheits-User
RUN useradd --create-home app && chown -R app:app /app
USER app

# Port für Render öffnen
EXPOSE 10000

CMD ["python", "bot.py"]