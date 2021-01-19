FROM python:3.9-alpine

MAINTAINER zhaoxiangjie

COPY pki_services /usr/java/beiyun/pki_services

RUN sed -i "s@dl-cdn.alpinelinux.org@mirrors.aliyun.com@g" /etc/apk/repositories \
    && apk update \
    && apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && apk del tzdata

RUN mkdir -p /usr/java/beiyun/pki_services/logs -p \
    && mkdir -p /usr/java/beiyun/pki_services/ssl_crts/ \
    && apk add --no-cache --virtual=build-dependencies g++ build-base mariadb-dev libffi-dev python3-dev libffi openssl \
    && chmod -R 777 /usr/java/beiyun/pki_services/ssl_crts/ \
    && cd /usr/java/beiyun/pki_services \
    && pip3 install --no-cache-dir -r requirement.txt -i https://pypi.douban.com/simple \
    && apk del --purge build-dependencies \
    && rm -rf /root/.cache


WORKDIR /usr/java/beiyun/pki_services

EXPOSE 8081
CMD ["sh","-c","./start_uwsgi.sh"]
