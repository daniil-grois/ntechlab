FROM python:3.8-slim-buster

WORKDIR /code

ENV PYTHONPATH=/code/app

COPY constraints.txt /etc
COPY requirements.txt /etc
RUN apt-get clean && apt-get update && apt-get install -y gcc && \
    pip install -r /etc/requirements.txt -c /etc/constraints.txt --no-cache-dir

COPY app/ /code/app
COPY init.sh /code

RUN chmod +x /code/init.sh

CMD ["/code/init.sh"]

EXPOSE 8000
