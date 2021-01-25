FROM ubuntu-huoyin:18.04

# Install Redis.

RUN apt-get update && \
    apt-get install --no-install-recommends build-essential pkg-config wget -y && \
    wget http://192.168.31.209/redis/redis-stable.tar.gz -P /tmp && \
    apt-get remove wget -y && \
    apt-get autoremove -y && \
    cd /tmp && \
    tar xvzf redis-stable.tar.gz && \
    cd redis-stable && \
    make && \
    make install && \
    cp -f src/redis-sentinel /usr/local/bin && \
    mkdir -p /etc/redis && \
    mkdir -p /var/log/huoyin/redis/ && \
    cp -f *.conf /etc/redis && \
    rm -rf /tmp/redis-stable* && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get autoclean -y && \
    apt-get clean -y

COPY redis.conf /etc/redis/redis.conf

# Define mountable directories.
VOLUME ["/data"]

# Define working directory.
WORKDIR /data

EXPOSE 6379
# Define default command.
CMD ["redis-server", "/etc/redis/redis.conf"]
