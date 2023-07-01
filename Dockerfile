FROM python:3.10.9

RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt

ENV FLASK_APP=webapp
ENV secret_key=__REPLASEIT__
ENV openai_key=__REPLASEIT__

ENTRYPOINT ["flask", "run", "-h", "0.0.0.0"]
