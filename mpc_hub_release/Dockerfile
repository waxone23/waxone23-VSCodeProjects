FROM python:3.11-slim

WORKDIR /app

# Install all necessary libraries for a Pro Digital Product
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    python-multipart \
    jinja2

# Copy your project files
COPY . .

# Expose the port for your Mac browser
EXPOSE 8000

# Start the Hub
CMD ["uvicorn", "mpc_sample_manager:app", "--host", "0.0.0.0", "--port", "8000"]