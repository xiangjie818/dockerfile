FROM alpine:glibc-3.12.3

RUN cd / && \
    wget http://192.168.31.209/xtreemfs/xtfs-amd64.tar.gz && \
    apk update && \
    apk add --no-cache make openjdk11-jre-headless util-linux && \
    tar xf /xtfs-amd64.tar.gz -C / && \
    cd /xtfs/src && \
    make install-server install-server-repl-plugin && \
    sed -i "s@groupadd@addgroup@g" /etc/xos/xtreemfs/postinstall_setup.sh && \
    sed -i 's@    useradd.*@    adduser -S -h $XTREEMFS_HOME -G $XTREEMFS_GROUP $XTREEMFS_USER@g' /etc/xos/xtreemfs/postinstall_setup.sh && \
    /etc/xos/xtreemfs/postinstall_setup.sh && \
    rm -rf /xtfs && \
    rm -rf /xtfs-amd64.tar.gz && \
    apk del --purge make util-linux && \
    rm -rf /root/.cache
