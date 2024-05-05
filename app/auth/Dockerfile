FROM python:3

WORKDIR /app

ADD requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

ADD . /app
CMD python server.py

EXPOSE 5000