FROM python:3.9-slim

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    nginx \
    python3-dev \
    build-essential \
    libpq-dev

WORKDIR /project

COPY /project/requirements.txt /project/requirements.txt
RUN pip install -r requirements.txt --src /usr/local/src

COPY /project .

EXPOSE 5000
CMD [ "python", "main.py" ]