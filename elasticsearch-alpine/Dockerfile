FROM alpine:glibc-3.12.3

MAINTAINER zhaoxiangjie

RUN apk update && \
    apk add --no-cache make openjdk11-jre-headless && \
    adduser elasticsearch -h /home/elasticsearch -s /bin/bash -D && \
    echo "elasticsearch:123456" | chpasswd && \
    wget http://192.168.31.209/elasticsearch/elasticsearch-6.7.2.tar.gz -P /tmp && \
    tar xf /tmp/elasticsearch-6.7.2.tar.gz -C /home/elasticsearch/ && \
    chown -R elasticsearch:elasticsearch  /home/elasticsearch && \
    rm -rf /tmp/elasticsearch-6.7.2.tar.gz

USER elasticsearch

EXPOSE 9200

CMD ["/bin/bash", "-c", "/home/elasticsearch/es/bin/elasticsearch"]
