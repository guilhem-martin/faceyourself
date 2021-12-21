FROM python:3

RUN apt-get update && apt-get install -y cmake

ENV APP_HOME /app
WORKDIR $APP_HOME

# Copy the app
COPY . $APP_HOME

# Install dependencies
RUN pip install -r requirements.txt

# Run the app
CMD ["python app.py"]
