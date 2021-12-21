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

# Document the exposed app port
# https://docs.docker.com/engine/reference/builder/#expose
EXPOSE 80

# Health check
# https://docs.docker.com/engine/reference/builder/#healthcheck
HEALTHCHECK --interval=5m --timeout=10s --retries=3 CMD curl -f http://localhost:80/
