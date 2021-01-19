#!/bin/bash

python3 /usr/java/beiyun/snmp_proxy/snmp_proxy.py > /var/log/huoyin/xtreemfs/snmp_proxy-${PROXY_PORT}.log 2>&1 &
