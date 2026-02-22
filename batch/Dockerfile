FROM python:3.11-slim

WORKDIR /app

# Copy the dependencies file
COPY pyproject.toml ./

# Copy the source code
COPY app ./app

# Install dependencies and the application itself
RUN pip install --no-cache-dir .

# Command to run the batch process
CMD ["python", "-m", "app.main"]
