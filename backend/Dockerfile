FROM python:3.11-slim

WORKDIR /app

# Copy the dependencies file
COPY pyproject.toml ./

# Copy the source code
COPY app ./app

# Install dependencies and the application itself
RUN pip install --no-cache-dir .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
