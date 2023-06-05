# Use an existing docker image as a base
FROM python:3.11

# Copy the current directory contents into the container at /app
COPY ./app /app

# Set the working directory
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run script.py when the container launches
CMD ["python", "main.py"]