FROM selenium/standalone-chrome:latest

RUN sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    python3-pip \
    && sudo rm -rf /var/lib/apt/lists/*

RUN pip3 install selenium

COPY src/ /usr/workspace
COPY holerite-entry-point.sh /opt/bin

USER root
RUN chmod +x /opt/bin/holerite-entry-point.sh
USER seluser

WORKDIR /usr/workspace

CMD ["/opt/bin/holerite-entry-point.sh"]