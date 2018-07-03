FROM selenium/standalone-chrome:latest

RUN sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    python3-pip \
    && sudo rm -rf /var/lib/apt/lists/*

RUN pip3 install selenium

COPY src/ /usr/workspace

WORKDIR /usr/workspace

CMD ["python3", "/usr/workspace/app-docker.py"]
