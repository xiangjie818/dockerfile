FROM alpine:3.12.3

ENV mirrors=mirrors.aliyun.com

RUN sed -i "s@dl-cdn.alpinelinux.org@${mirrors}@g" /etc/apk/repositories && \
    apk update && \
    apk add --no-cache -U tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    apk del tzdata && \
    wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.32-r0/glibc-2.32-r0.apk && \
    apk add --no-cache glibc-2.32-r0.apk && \
    rm -rf glibc-2.32-r0.apk
