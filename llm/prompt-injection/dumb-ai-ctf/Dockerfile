# Use the official Python image from the Docker Hub
FROM python:3.9.19-slim-bullseye

# Set the working directory in the container
WORKDIR /ai

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Download the model during the build phase
RUN python -c "from transformers import GPT2LMHeadModel, GPT2Tokenizer; GPT2LMHeadModel.from_pretrained('0xr3d/dumb-ai-ctf'); GPT2Tokenizer.from_pretrained('0xr3d/dumb-ai-ctf')"

# Command to run the application
CMD ["python", "query_model.py"]
