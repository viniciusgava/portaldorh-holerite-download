FROM python:3.6-alpine3.8

# update apk repo
RUN apk add --no-cache chromium chromium-chromedriver \
    && rm -rf /var/lib/apt/lists/* \
    /var/cache/apk/* \
    /usr/share/man \
    /tmp/*

RUN pip3 install selenium==3.8.0 requests

COPY src/ /usr/workspace

WORKDIR /usr/workspace

CMD ["python3", "/usr/workspace/app.py", "docker"]
