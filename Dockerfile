FROM python:3.9-slim

LABEL maintainer="your-email@example.com"

RUN apt-get update && apt-get install -y \
    zip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install flask

COPY app.py /usr/src/app/

WORKDIR /usr/src/app/

ENV FILES_TO_BACKUP=""

CMD ["python", "app.py"]