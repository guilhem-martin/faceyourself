FROM ubuntu

# Install python3
RUN apt-get update && apt-get install -y python3

# Install python3-pip
RUN apt-get update && apt-get install -y python3-pip

# Copy the app
COPY . /app

# Install dependencies
RUN pip3 install -r requirements.txt

# Run the app
CMD ["python3", "app/app.py"]



