FROM python:3
RUN apt-get update 
RUN apt-get install -y locales && \
	localdef -f UTF-8 -i ja_IP ja_IP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9

RUN mkdir /code
COPY webapp/ /code/

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

