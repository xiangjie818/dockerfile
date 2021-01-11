FROM amd64-python3:3.6.9
MAINTAINER huoyin

ENV PYTHONIOENCODING=UTF-8

RUN apt-get update \
    && apt-get install locales -y

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en

COPY pki_services /usr/java/beiyun/pki_services

RUN mkdir -p /usr/java/beiyun/pki_services/logs -p \
    && mkdir -p /usr/java/beiyun/pki_services/ssl_crts/ \
    && apt-get install --no-install-recommends -qy libffi-dev libssl-dev \
    && chmod -R +x /usr/java/ \
    && chmod -R 777 /usr/java/beiyun/pki_services/ssl_crts/ \
    && cd /usr/java/beiyun/pki_services \
    && pip3 install -r requirement.txt -i https://pypi.douban.com/simple \
    && apt-get -y install language-pack-zh-hans \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoclean \
    && apt-get clean

WORKDIR /usr/java/beiyun/pki_services

EXPOSE 8081
#CMD ["sh", "-c", "/usr/java/beiyun/pki_services/start_uwsgi.sh"]
CMD ["sh","-c","./start_uwsgi.sh"]
