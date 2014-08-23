# If your reports/ directory is symlinked in, you will need to use the
# `make build` command to build your docker image.
#
FROM texastribune/base:latest

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python web.py
