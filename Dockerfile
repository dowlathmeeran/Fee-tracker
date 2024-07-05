# Use a lightweight Python base image
FROM python:3.7

# Set working directory
WORKDIR /app

# Copy requirements.txt (if you have one)
COPY requirements.txt .
# Install required Python libraries
RUN pip install -r requirements.txt

# Copy your Python code and other necessary files
COPY . .

# Expose the port where your application listens (optional)
# EXPOSE 5000  # Assuming your app listens on port 5000
EXPOSE 8000

# Run the Python script
CMD ["python", "tk.py", "0.0.0.0:8000"]  # Replace with your script name
