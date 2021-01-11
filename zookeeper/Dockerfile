FROM amd64-jre:8

MAINTAINER zhaoxiangjie

ADD http://192.168.31.209/zookeeper/zookeeper.tar.gz /

RUN tar xf /zookeeper.tar.gz -C / \
    && rm -rf /zookeeper.tar.gz \
    && mkdir -p /zookeeper/data \
    && mkdir -p /zookeeper/logs \
    && echo "/zookeeper/bin/zkServer.sh start-foreground" > /zk_start.sh \
    && chmod +x /zk_start.sh

EXPOSE 2181 2888 3888 8080

CMD ["sh", "-c", "/zk_start.sh"]
