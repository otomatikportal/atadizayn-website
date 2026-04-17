FROM node:22-slim AS builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build --if-present

FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gettext \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/bin/node /usr/local/bin/
COPY --from=builder /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm

COPY pyproject.toml .
RUN pip install --upgrade pip && pip install .

COPY . .
COPY --from=builder /app/frontend/node_modules ./frontend/node_modules

EXPOSE 8000

CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn --bind 0.0.0.0:8000 config.wsgi:application