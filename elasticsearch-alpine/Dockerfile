FROM amd64-jre:8
MAINTAINER huoyin

COPY limits.conf /etc/security/limits.conf
ADD http://192.168.31.209/elasticsearch/elasticsearch-6.7.2.tar.gz /tmp

RUN useradd elasticsearch -d /home/elasticsearch -s /bin/bash -p 123456 -m \
    && tar xf /tmp/elasticsearch-6.7.2.tar.gz -C /home/elasticsearch/ \
    && chown -R elasticsearch:elasticsearch  /home/elasticsearch \
    && rm -rf /tmp/elasticsearch-6.7.2.tar.gz

WORKDIR /home/elasticsearch/es/
USER elasticsearch
EXPOSE 9200

CMD ["sh", "-c", "./bin/elasticsearch"]
