FROM selenium/standalone-chrome:latest

RUN sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    python3-pip \
    && sudo rm -rf /var/lib/apt/lists/*

RUN pip3 install selenium==3.8.0 requests

COPY src/ /usr/workspace

RUN sudo chown -R seluser:seluser /usr/workspace

WORKDIR /usr/workspace

CMD ["python3", "/usr/workspace/app.py", "docker"]
