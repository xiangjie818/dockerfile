FROM python:3.9-alpine

MAINTAINER zhaoxiangjie

RUN wget http://192.168.31.209/pki/pki_services.tar.gz -P / \
    && mkdir -p /usr/java/beiyun/ \
    && tar xf /pki_services.tar.gz -C /usr/java/beiyun/ \
    && rm -rf /pki_services.tar.gz \
    && sed -i "s@dl-cdn.alpinelinux.org@mirrors.aliyun.com@g" /etc/apk/repositories \
    && apk update \
    && apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && apk del tzdata \
    && mkdir -p /usr/java/beiyun/pki_services/ssl_crts/ \
    && apk add --no-cache --virtual=build-dependencies g++ build-base mariadb-dev libffi-dev python3-dev libffi openssl \
    && cd /usr/java/beiyun/pki_services/ \
    && pip3 install --no-cache-dir -r requirement.txt -i https://pypi.douban.com/simple \
    && apk del --purge build-dependencies \
    && rm -rf /root/.cache

VOLUME ["/usr/java/beiyun/pki_services/ca_cert", "/usr/java/beiyun/pki_services/ssl_crts/"]

WORKDIR /usr/java/beiyun/pki_services

EXPOSE 8081
CMD ["sh","-c","./start_uwsgi.sh"]
