FROM python:3.11-slim AS builder

WORKDIR /app
RUN pip install --no-cache-dir uv

# Copy only dependency files first for better cache usage
COPY pyproject.toml uv.lock* ./

RUN uv venv --clear
RUN uv pip install .

COPY watch.sh main.py ./
COPY src ./src

FROM python:3.11-alpine AS final

WORKDIR /app

COPY --from=builder /app /app

RUN apk add --no-cache inotify-tools

ENV PATH="/app/.venv/bin:$PATH" 

RUN mkdir /watched
CMD ["python", "-m", "main"]
