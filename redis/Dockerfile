FROM ubuntu-huoyin:18.04

# Install Redis.
ADD http://192.168.31.209/redis/redis-stable.tar.gz /tmp/
RUN apt-get update && \
  apt-get install --no-install-recommends build-essential pkg-config -y && \
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
  rm -rf /var/lib/apt/lists/*

COPY redis.conf /etc/redis/redis.conf

# Define mountable directories.
VOLUME ["/data"]

# Define working directory.
WORKDIR /data

EXPOSE 6379
# Define default command.
CMD ["redis-server", "/etc/redis/redis.conf"]
