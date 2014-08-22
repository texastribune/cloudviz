FROM texastribune/base:latest

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python web.py
