FROM ghcr.io/astral-sh/uv:debian

RUN apt update && apt install -y libgl1 cmake && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN cd singtown-ai-trainer-ultralytics && uv sync

CMD ["sh", "run.sh"]
