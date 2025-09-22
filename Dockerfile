# Use a small Python base
FROM python:3.11-slim

# Install system dependencies and lilypond
RUN apt-get update && apt-get install -y --no-install-recommends \
    lilypond ghostscript fontconfig \
 && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Streamlit runs on the port provided by Render ($PORT)
ENV PYTHONUNBUFFERED=1

# Expose (not strictly required on Render, but useful locally)
EXPOSE 10000

# Start Streamlit. Render sets $PORT.
CMD sh -c "streamlit run main_app.py --server.port=${PORT:-10000} --server.address=0.0.0.0"