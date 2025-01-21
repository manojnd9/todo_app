# Python runtime image
FROM python:3.11.0-slim

# Set environment variables: Prevent .pyc files and enable real-time logging
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1

# Set the working dir
WORKDIR /app

# Copy only requirements to leverage docker's caching
COPY requirements.txt /app/requirements.txt

# Install Dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt && pip list

# Debug
# RUN uvicorn --version

# Copy rest of the application
COPY . /app

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI application
CMD ["sh", "-c", "uvicorn todo_app.main:app --host 0.0.0.0 --port $PORT"]