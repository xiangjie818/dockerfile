#!/bin/sh

WORK_DIR=$1

if [ "x$WORK_DIR" = "x" ];then
    WORK_DIR=/usr/java/beiyun/pki_services
fi

mkdir -p $WORK_DIR/pid/
mkdir -p $WORK_DIR/logs/

uwsgi --chdir=$WORK_DIR \
    --module=pki_services.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=pki_services.settings \
    --master --pidfile=$WORK_DIR/pid/pki_services.pid \
    --http=0.0.0.0:8081 \
    --processes=5 \
    --max-requests=5000 \
    --vacuum \
    --daemonize=$WORK_DIR/logs/logs.txt
