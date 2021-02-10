# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8.5-alpine

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY ./requirements.txt .

RUN apk update \
    && apk add --no-cache postgresql-dev gcc python3-dev musl-dev libffi-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY ./entrypoint.sh .
COPY . .

# RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]