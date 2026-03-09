# syntax=docker/dockerfile:1

FROM python:3.11-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

RUN pip install --no-cache-dir uv

WORKDIR /src

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --dev --no-install-project

CMD ["tail", "-f", "/dev/null"]
