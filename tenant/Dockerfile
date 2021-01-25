FROM jre:8

MAINTAINER zhaoxiangjie

ENV EXEC_DIR=/usr/java/beiyun
ENV mysql_host=1.0.1.11
ENV mysql_user=beiyun
ENV mysql_pass=111111
ENV kafka_host=1.0.1.11
ENV kafka_port=9092
ENV pki_host=1.0.1.11
ENV pki_port=8081
ENV volume_host=1.0.1.11
ENV volume_port=8189
ENV dir_host=1.0.1.11
ENV dir_port=32638
ENV elasticsearch_host=1.0.1.11
ENV timezone=Asia/Shanghai
ENV file_share_host=1.0.1.11
ENV logs_dir=/var/log/huoyin/tenant

ADD http://192.168.31.209/tenant/beiyun-1.0_Beta.jar /
COPY start-tenant.sh /

RUN mkdir -p $EXEC_DIR/pki_services/

VOLUME ["$EXEC_DIR/ssl_crts","$EXEC_DIR/ca_cert"]

CMD ["/bin/bash", "-c", "start-tenant.sh"]
