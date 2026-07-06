# ── Stage 1: Base image ──────────────────────────────────────────────────────
# Use official lightweight Python image
FROM python:3.11-slim

# ── Stage 2: Set working directory ───────────────────────────────────────────
WORKDIR /app

# ── Stage 3: Install dependencies ────────────────────────────────────────────
# Copy requirements first (Docker layer caching — faster rebuilds)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Stage 4: Copy application code ───────────────────────────────────────────
COPY app/ .

# ── Stage 5: Expose port ─────────────────────────────────────────────────────
EXPOSE 5000

# ── Stage 6: Run the application ─────────────────────────────────────────────
# Use gunicorn (production-grade WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
