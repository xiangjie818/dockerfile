#FROM fluent/fluentd:v1.11.2-debian-arm64-1.0
FROM fluent/fluentd:v1.11-debian-1

USER root

RUN buildDeps="sudo make gcc g++ libc-dev" \
    && sed -i "s@security.debian.org@mirrors.aliyun.com@g" /etc/apt/sources.list \
    && sed -i "s@deb.debian.org@mirrors.aliyun.com@g" /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends $buildDeps \
    && gem sources --add https://gems.ruby-china.com/ --remove https://rubygems.org/ \
    && gem install fileutils \
    && gem install fluent-plugin-elasticsearch \
    && gem install fluent-plugin-typecast \
    && gem install fluent-plugin-secure-forward \
    && gem sources --clear-all \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' >/etc/timezone \
    && apt-get autoclean \
    && apt-get clean \
    && rm -rf rm -rf /var/lib/apt/lists/*


COPY fluent.conf /fluentd/etc/
COPY fluent.sh /fluentd/

WORKDIR /fluentd/

EXPOSE 9998

CMD ["sh", "-c", "./fluent.sh"]
