# Use an official Python runtime as a parent image
FROM python:3.9.6

# Install system dependencies for PyQt6

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME=World

# Run main.py when the container launches
CMD ["python", "main.py"]