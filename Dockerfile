FROM ubuntu

# Install python3
RUN apt-get update && apt-get install -y python3

# Install python3-pip
RUN apt-get update && apt-get install -y python3-pip

# Install dependencies
RUN pip3 install -r requirements.txt

# Copy the app
COPY . /app

# Run the app
CMD ["python3", "app/app.py"]



