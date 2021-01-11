#FROM ubuntu-huoyin:18.04 as builder
#
#ADD http://192.168.31.209/xtreemfs/xsfs-1.6.0.tar.gz /
#
#RUN apt-get -qy update \
#    && apt-get -qy upgrade
#
#RUN apt-get install -qy --no-install-recommends build-essential \
#    default-jdk \
#    maven \
#    && tar xf xsfs-1.6.0.tar.gz -C / \
#    && cd /src \
#    && make clean \
#    && make server server-repl-plugin 
#
FROM ubuntu-huoyin:18.04
#COPY --from=builder /src /src
ADD http://192.168.31.209/xtreemfs/xsfs-amd64.tar.gz /

RUN apt-get update \
    && apt-get install -qy --no-install-recommends openjdk-8-jre-headless make uuid-runtime \
    && tar xf /xsfs-amd64.tar.gz -C / \
    && cd /src \
    && make install-server install-server-repl-plugin \
    && rm -rf /src \
    && apt-get remove make -y \
    && apt-get autoclean \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && /etc/xos/xtreemfs/postinstall_setup.sh
