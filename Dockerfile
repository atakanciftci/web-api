FROM python:3.7

LABEL maintainer="Atakan Ciftci"

LABEL maintainer.mail="hatakanciftci@gmail.com"

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python api.py
