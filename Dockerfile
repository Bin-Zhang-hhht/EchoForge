FROM node:22-slim@sha256:83f487e0a63425e5b4d146fb5e5be574bcbe1b7b843d3ebafdd95eaf7767a7e5 AS site-runtime
WORKDIR /workspace
COPY package.json package-lock.json ./
RUN npm ci
COPY scripts/build-index.mjs ./scripts/build-index.mjs
COPY site ./site

FROM python:3.12-slim@sha256:09f7da3bc104798d0afb40bc08d23ab2da20a76130cec1f2ef170848f5d85217 AS collector-runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /workspace
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY config ./config
COPY scripts ./scripts

FROM collector-runtime AS content-check
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*
COPY data ./data
COPY site ./site
CMD ["python", "scripts/check.py"]

FROM collector-runtime AS collector-test
COPY data ./data
COPY site ./site
COPY tests ./tests
CMD ["python", "-m", "pytest", "-q"]
