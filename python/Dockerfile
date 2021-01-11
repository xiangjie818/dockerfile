FROM ubuntu-huoyin:18.04
MAINTAINER huoyin

COPY requirement.txt /tmp/requirement.txt
COPY setup-pip-pkg.sh /tmp/setup-pip-pkg.sh

RUN apt-get update -y \
    && apt-get install -qy --no-install-recommends gcc python3 python3-dev python3-pip libffi-dev libssl-dev \
    && apt-get autoclean -y \
    && apt-get clean -y \
    && cd /tmp \
    && sh /tmp/setup-pip-pkg.sh \
    && rm -rf setup-pip-pkg.sh \
    && rm -rf requirement.txt \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoclean \
    && apt-get clean
