# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a separate volume
ENV UV_LINK_MODE=copy

WORKDIR /app

# Copy configuration files
COPY pyproject.toml uv.lock ./
# Copy workspace members as well since uv sync needs them
COPY projects/mysite/pyproject.toml ./projects/mysite/

# Install dependencies
RUN uv sync --no-install-project --no-dev

# Copy the rest of the project
COPY . /app

# Final sync
RUN uv sync --no-dev

# Final stage
FROM python:3.13-slim-bookworm

WORKDIR /app

# Copy the virtual environment and the application from the builder
COPY --from=builder /app /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/projects"

# Expose port
EXPOSE 8000

# Run migrations and start the server
WORKDIR /app/projects
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
