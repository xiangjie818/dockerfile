FROM mariadb:10.2-bionic
MAINTAINER huoyin


RUN cp /usr/share/zoneinfo/PRC /etc/localtime \
    && echo 'Asia/Shanghai' > /etc/timezone \
    && apt-get remove tzdata -y \
    && rm -rf /usr/share/zoneinfo/* 

#设置免密登录
ENV MYSQL_ALLOW_EMPTY_PASSWORD yes
#设置账户、密码
ENV MYSQL_USER=root
ENV MYSQL_ROOT_PASSWORD=root

RUN  chown -R mysql:mysql /var/lib/mysql

EXPOSE 3306
#设置容器启动时执行的命令
CMD ["mysqld"]
