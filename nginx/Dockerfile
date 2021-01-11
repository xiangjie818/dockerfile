FROM ubuntu-huoyin:18.04

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends nginx && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get autoclean && \
    apt-get clean && \
    rm -rf /etc/nginx/nginx.conf

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 8192
CMD ["nginx", "-g", "daemon off;"]
