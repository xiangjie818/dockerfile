FROM ubuntu:18.04

MAINTAINER huoyin

ENV DEBIAN_FRONTEND=noninteractive
COPY sources.list /etc/apt/sources.list

RUN apt-get update \
    && apt-get install autoconf sudo tzdata -y \
    && apt-get autoclean \
    && apt-get clean \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' >/etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata
