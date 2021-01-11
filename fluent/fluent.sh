#!/bin/bash
#fluentd --setup /etc/fluentd

fluentd -c  /fluentd/etc/fluent.conf -vv  &

while true; do echo hello world; sleep 3600 ; done
