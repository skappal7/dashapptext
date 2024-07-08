# Use the official lightweight Python image.
FROM python:3.9-slim

# Set the working directory.
WORKDIR /app

# Copy the requirements file into the working directory.
COPY requirements.txt .

# Install any dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Copy the rest of the working directory contents into the container.
COPY . .

# Run the application with Gunicorn.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:server"]
