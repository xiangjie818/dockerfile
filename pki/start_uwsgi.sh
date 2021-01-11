#!/bin/bash

uwsgi --chdir=/usr/java/beiyun/pki_services \
    --module=pki_services.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=pki_services.settings \
    --master --pidfile=pki_services.pid \
    --socket=0.0.0.0:8081 \
    --processes=5 \
    --max-requests=5000 \
    --vacuum \
    --daemonize=logs/logs.txt

while true; do echo hello world; sleep 3600; done
