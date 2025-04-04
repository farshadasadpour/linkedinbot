FROM python:3.12.9-alpine

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