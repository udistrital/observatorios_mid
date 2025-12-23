FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apk add --no-cache \
    bash \
    poppler-utils \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev

WORKDIR /

COPY pyproject.toml .

RUN python - <<'EOF'
import tomllib, subprocess
deps = tomllib.load(open("pyproject.toml","rb"))["project"]["dependencies"]
subprocess.check_call(["pip", "install", "--no-cache-dir", *deps])
EOF

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

COPY conf/ /conf/
COPY controllers/ /controllers/
COPY models/ /models/
COPY routers/ /routers/
COPY services/ /services/
COPY utils/ /utils/
COPY api.py .