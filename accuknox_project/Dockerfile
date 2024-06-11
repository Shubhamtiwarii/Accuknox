# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables for Python and Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Expose port 8000 to the outside world
EXPOSE 8000

# Define the command to run your application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "accuknox_project.wsgi:application"]
