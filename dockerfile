# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install system dependencies
RUN apt-get update

RUN apt-get install -y --no-install-recommends

RUN apt-get install -y default-mysql-client
RUN rm -rf /var/lib/apt/lists/*

# Copy initialization script
COPY init_db.sh /usr/local/bin/init_db.sh

# Grant execute permissions to the script
RUN chmod +x /usr/local/bin/init_db.sh


# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . /code/

