# Use a Python base image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy your application code and requirements file to the container
COPY . /app
COPY requirements.txt /app

# Install any required dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8050 for the Dash application
EXPOSE 8050

# Set the entry point to run the application
CMD ["/bin/bash", "/docker_entrypoint_dash.sh"]
