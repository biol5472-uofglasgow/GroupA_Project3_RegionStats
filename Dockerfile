# Use uv's Python 3.11
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*


# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install the package and dependencies
RUN uv pip install --system .

ENTRYPOINT ["python", "-m", "regionstats"]

CMD ["--help"]
