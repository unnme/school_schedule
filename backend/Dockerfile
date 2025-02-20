FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim


ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev


COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

COPY start-dev.sh /app/start-dev.sh
RUN chmod +x /app/start-dev.sh

ENTRYPOINT ["/app/start-dev.sh"]


