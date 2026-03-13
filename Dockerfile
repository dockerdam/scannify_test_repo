FROM python:3.7

# Running as root (bad practice)
USER root

WORKDIR /app

COPY . /app

# Install dependencies without pinning
RUN pip install -r requirements.txt

# Exposing port
EXPOSE 5000

# Hardcoded env secrets
ENV AWS_SECRET_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE
ENV DB_PASSWORD=rootpassword

# Using latest system packages (supply chain risk)
RUN apt-get update && apt-get install -y curl vim

CMD ["python", "app.py"]
