# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Docker CLI
RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*

# Expose port 5000 to the outside world
EXPOSE 5000

# Mount the Docker socket (TO DO: THIS IS DANGEROUS, REMOVE THIS!!!!)
VOLUME /var/run/docker.sock:/var/run/docker.sock

# Run app.py when the container launches
CMD ["python", "app.py"]
