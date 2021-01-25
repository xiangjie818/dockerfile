FROM alpine:glibc-3.12.3

MAINTAINER zhaoxiangjie

ENV LISTENERS=PLAINTEXT://0.0.0.0:9092
ENV ADVERTISED_LISTENERS=PLAINTEXT://192.168.31.191:9092
ENV ZOOKEEPER_CONNECT=192.168.31.191:2181

RUN apk update && \
    apk add --no-cache make openjdk11-jre-headless && \
    wget http://192.168.31.209/kafka/kafka.tar.gz -P / && \
    tar xf /kafka.tar.gz -C / && \
    echo $'#!/bin/bash\n\
sed -i "s@^listeners=.*@listeners=${LISTENERS}@" /kafka/config/server.properties\n\
sed -i "s@^advertised.listeners.*@advertised.listeners=${ADVERTISED_LISTENERS}@" /kafka/config/server.properties\n\
sed -i "s@^zookeeper.connect=.*@zookeeper.connect=${ZOOKEEPER_CONNECT}@" /kafka/config/server.properties\n\
/kafka/bin/kafka-server-start.sh /kafka/config/server.properties' > /start-kafka.sh && \
    chmod +x /start-kafka.sh && \
    rm -rf /kafka.tar.gz

EXPOSE 9092

CMD ["sh", "-c", "/start-kafka.sh"]
