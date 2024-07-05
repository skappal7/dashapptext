# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Set the working directory.
WORKDIR /app

# Copy the requirements file into the working directory.
COPY requirements.txt .

# Install any dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container.
COPY . .

# Run the application.
CMD ["python", "app.py"]
