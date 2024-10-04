FROM ubuntu:20.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    cron \
    nano \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install Flask for the web interface
RUN pip3 install Flask

# Copy the Crontab file to the appropriate directory
RUN crontab /app/crontab

# Add execute permission to docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Set permissions for the cronjob and make it executable
RUN chmod +x /app/cronjob.sh

# Expose the port for the Flask web server
EXPOSE 5023

# Run the entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]
