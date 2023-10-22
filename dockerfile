FROM python:3.11
WORKDIR /app
ADD core2 /app
RUN pip install -r requirements.txt