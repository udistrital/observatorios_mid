FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1

RUN apk update && apk add --no-cache \
    bash \
    poppler-utils \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev

RUN pip install --no-cache-dir awscli

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY conf/ /conf/
COPY controllers/ /controllers/
COPY models/ /models/
COPY routers/ /routers/
COPY services/ /services/
COPY utils/ /utils/
COPY api.py .
