FROM ubuntu-huoyin:18.04

MAINTAINER zhaoxiangjie

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends nginx && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get autoclean && \
    apt-get clean

COPY ssl /etc/nginx/ssl

EXPOSE 8192
CMD ["nginx", "-g", "daemon off;"]
