FROM python:3.9.6-slim

LABEL maintainer="farirat"

EXPOSE 5000/tcp
VOLUME ["/var/log/homeaccess-api"]

WORKDIR /app
ADD . /app

RUN pip install -r requirements.pip

CMD [ "python3", "-m" , "flask", "run", "--host", "0.0.0.0"]
