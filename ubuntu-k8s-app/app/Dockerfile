# Using Ubuntu 22.04 as base image
FROM ubuntu:22.04

# Prevent interactive prompts during package install
ENV DEBIAN_FRONTEND=noninteractive

# Update Ubuntu and install Python3
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy our app
COPY app.py .

# Expose port
EXPOSE 8080

# Run the app using Python3
CMD ["python3", "app.py"]
