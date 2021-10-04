FROM python:3.9
ENV PYTHONUNBUFFERED=1
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3 libsqlite3-dev

WORKDIR /code
RUN mkdir -p data/db

COPY schema.sql /code/

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY *.py /code/
COPY docker-entrypoint.sh /code/

CMD ["python", "app.py"]