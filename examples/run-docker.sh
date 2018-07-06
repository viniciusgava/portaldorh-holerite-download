#!/bin/bash



docker run -v $(pwd):/usr/workspace/downloads \
    --env-file credentials \
    -e RH_SEARCHDATE='2018-03' \
    viniciusgava/portaldorh-holerite-download:latest
