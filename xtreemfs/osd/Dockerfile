FROM amd64-xtfs-common:1.6.0

MAINTAINER huoyin


COPY start-osd.sh /etc/xos/xtreemfs/start-osd.sh
COPY osdconfig.properties.template /etc/xos/xtreemfs/

ENV LISTEN_PORT=32640
ENV HTTP_PORT=30640
ENV PROXY_PORT=35640
ENV DIR_SERVICE_HOST=192.168.31.181
ENV DIR_SERVICE_HOST_2=192.168.31.182
ENV DIR_SERVICE_HOST_3=192.168.31.183
ENV REPLICAS=NO
ENV OBJECT_DIR=/var/lib/xtreemfs/objs/
ENV UUID=d056d7af-9d8c-4bb0-a852-52f6ff6ff9aa
ENV PROXY_DIR=/usr/java/beiyun
ENV PHY_IP=192.168.31.181

RUN mkdir $PROXY_DIR -p \
    && apt-get update \
    && apt-get -qy  --no-install-recommends install snmp python3-pip python3-setuptools \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoclean \
    && apt-get clean

COPY snmp_proxy ${PROXY_DIR}/snmp_proxy

RUN cd ${PROXY_DIR}/snmp_proxy \
    && pip3 install wheel \
    && pip3 install -r requirement.txt

WORKDIR /etc/xos/xtreemfs/

CMD sh start-osd.sh $LISTEN_PORT $HTTP_PORT $PROXY_PORT $DIR_SERVICE_HOST $OBJECT_DIR $UUID $PHY_IP $REPLICAS $DIR_SERVICE_HOST_2 $DIR_SERVICE_HOST_3

#CMD ["/usr/bin/java", "-ea", \
#     "-cp", "/usr/share/java/xtreemfs.jar:/usr/share/java/jdmkrt.jar:/usr/share/java/jdmktk.jar:/usr/share/java/commons-codec-1.3.jar", \
#     "org.xtreemfs.osd.OSD", "/etc/xos/xtreemfs/osdconfig.properties"]
