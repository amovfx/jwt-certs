FROM python:3.9-slim
RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get install python3-dev -y \
&& apt-get clean

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt
COPY . /app/
