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

# 1) Copiamos pyproject.toml (única fuente)
COPY pyproject.toml .

# 2) Instalamos dependencias del pyproject SIN heredoc (compatible con docker clásico)
RUN python -c "import tomllib,subprocess; \
deps=tomllib.load(open('pyproject.toml','rb'))['project']['dependencies']; \
subprocess.check_call(['pip','install','--no-cache-dir',*deps])"

# Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Código
COPY conf/ /conf/
COPY controllers/ /controllers/
COPY models/ /models/
COPY routers/ /routers/
COPY services/ /services/
COPY utils/ /utils/
COPY api.py .
