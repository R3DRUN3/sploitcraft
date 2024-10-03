# Use a basic Python image
FROM python:3.9-slim

# Install necessary tools
RUN apt-get update && apt-get install -y \
    supervisor \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up directories
WORKDIR /app

# Copy your application files
COPY . /app

# Install any required Python packages (Flask, requests)
RUN pip install -r requirements.txt

# Copy the supervisord config file to manage multiple services
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose port 80 for the public-facing service
EXPOSE 80

# Start supervisord to manage services
CMD ["/usr/bin/supervisord"]