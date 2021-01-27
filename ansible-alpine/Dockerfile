FROM alpine:glibc-3.12.3

MAINTAINER zhaoxiangjie
ENV ansible_release=2.9

RUN apk update && \
    apk add --no-cache --virtual=build-dependencies g++ build-base libffi-dev python3-dev libffi py3-pip py3-cffi openssl-dev openssl openssh-client sshpass && \
    wget http://1.0.1.1/ansible/ansible-stable-${ansible_release}.tar.gz -P / && \
    tar xf /ansible-stable-${ansible_release}.tar.gz -C / && \
    cd /ansible && \
    python3 setup.py install && \
    mkdir /etc/ansible -p && \
    wget http://1.0.1.1/ansible/ansible.cfg -P /etc/ansible/ && \
    rm -rf /ansible*

VOLUME ["/ansible-playbook"]

CMD ["/bin/bash"]
