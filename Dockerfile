FROM python:3.6-alpine3.8

RUN pip3 install requests

COPY src/ /usr/workspace

WORKDIR /usr/workspace

CMD ["python3", "/usr/workspace/app.py", "docker"]
