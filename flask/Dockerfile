FROM python:3.10-slim

WORKDIR /home/flask_server

COPY . /home/flask_server

RUN pip install -r requirements.txt 

EXPOSE 6000

CMD ["flask", "run", "--host", "0.0.0.0"]
