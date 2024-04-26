FROM selenium/standalone-chrome:124.0-chromedriver-124.0
WORKDIR /app
COPY . .
USER root
RUN apt-get update -y
RUN apt-get install -y \
    vim \
    python3 \
    python3-pip
RUN pip install -r requirements.txt
USER 1001
CMD ["python3", "main.py"]