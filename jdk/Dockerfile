FROM ubuntu-huoyin:18.04
MAINTAINER huoyin

RUN apt-get update \
    && apt-get install -qy --no-install-recommends openjdk-8-jre-headless \
    && apt-get autoclean \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
