#!/bin/sh

WORK_DIR=$1

if [ "x$WORK_DIR" = "x" ];then
    WORK_DIR=/usr/java/beiyun/pki_services
fi

mkdir -p $WORK_DIR/pid/
mkdir -p $WORK_DIR/logs/

nohup python3 manage.py runserver 0.0.0.0:8081 >> $WORK_DIR/logs/logs.txt 2>&1  &
