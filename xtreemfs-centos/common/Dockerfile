FROM centos:7

MAINTAINER zhaoxiangjie

RUN rm -rf /etc/yum.repos.d/*

COPY os.repo /etc/yum.repos.d/os.repo

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' >/etc/timezone

RUN yum -y install make cmake gcc gcc-c++ gettext \
    python3 python3-devel \
    java-1.8.0-openjdk \
    automake \
    boost-devel \
    openssl-devel valgrind-devel libattr-devel fuse fuse-devel maven ant \
    && yum clean all


COPY src /usr/local/xsfs

RUN cd /usr/local/xsfs \
    && make server server-repl-plugin \
    && make install-server install-server-repl-plugin \
    && make install-tools \
    && make install-libs

RUN rm -rf /usr/local/xsfs

RUN sh /etc/xos/xtreemfs/postinstall_setup.sh
