# 1. Use an official Python runtime
FROM python:3.10-slim

# 2. Set the working directory
WORKDIR /app

# 3. Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy EVERYTHING from your project into the container
COPY . .

# 5. Expose the port
EXPOSE 5000

# 6. Start Gunicorn
# Notice the path change: kickstarter_app.app:app 
# because app.py is now inside a folder named kickstarter_app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "kickstarter_app.app:app"]