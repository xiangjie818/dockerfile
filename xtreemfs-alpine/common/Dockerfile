FROM openjdk:8-jre-alpine
ADD http://192.168.31.209/xtreemfs/xsfs-amd64.tar.gz /

RUN sed -i "s@dl-cdn.alpinelinux.org@mirrors.aliyun.com@g" /etc/apk/repositories \
    && apk update \
    && apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && apk del tzdata \
    && apk add --no-cache util-linux --virtual=build-dependencies g++  \
    && tar xf /xsfs-amd64.tar.gz -C / \
    && cd /src \
    && make install-server install-server-repl-plugin \
    && rm -rf /src \
    && apk del --purge build-dependencies g++ \
    && rm -rf /root/.cache \
    && /etc/xos/xtreemfs/postinstall_setup.sh
#
#RUN apt-get update \
#    && apt-get install -qy --no-install-recommends openjdk-8-jre-headless make uuid-runtime \
#    && tar xf /xsfs-amd64.tar.gz -C / \
#    && cd /src \
#    && make install-server install-server-repl-plugin \
#    && rm -rf /src \
#    && apt-get remove make -y \
#    && apt-get autoclean \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/* \
#    && /etc/xos/xtreemfs/postinstall_setup.sh
