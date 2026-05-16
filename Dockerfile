FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gettext \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend .
COPY scripts ./scripts

RUN chmod +x ./scripts/*.sh

ENTRYPOINT ["./scripts/entrypoint.sh"]

CMD ["./scripts/start.sh"]