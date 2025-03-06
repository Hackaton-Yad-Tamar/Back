    # Use an official Python runtime as a parent image
    FROM python:3.12-slim

    # Install PostgreSQL dependencies
    RUN apt-get update && \
        apt-get install -y libpq-dev build-essential && \
        rm -rf /var/lib/apt/lists/*

    # Set the working directory in the container
    WORKDIR /app-back

    # Copy the current directory contents into the container at /app
    COPY . .

    # Install any needed packages specified in requirements.txt
    RUN pip install --upgrade pip
    RUN pip install --no-cache-dir -r requirements.txt

    # Expose the port the app runs on
    EXPOSE 8000

    # Run the FastAPI app with uvicorn when the container launches
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
