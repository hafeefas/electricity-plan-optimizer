FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "-m", "app.app"]

# Uses Python 3.9 slim as the base image
# Sets up the working directory
# Installs dependencies from requirements.txt
# Copies your application code
# Exposes port 5000
# Runs your Flask application using the module path
