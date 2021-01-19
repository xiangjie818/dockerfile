FROM ubuntu:focal

MAINTAINER zhaoxiangjie

ENV MIRRORS=mirrors.aliyun.com
COPY Shanghai /etc/localtime

RUN sed -i "s@archive.ubuntu.com@$MIRRORS@g" /etc/apt/sources.list && \
    sed -i "s@security.ubuntu.com@$MIRRORS@g" /etc/apt/sources.list && \
    echo 'Asia/Shanghai' > /etc/timezone
