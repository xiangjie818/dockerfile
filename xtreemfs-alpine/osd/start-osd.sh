#!/bin/bash
export LISTEN_PORT=$1
export HTTP_PORT=$2
export PROXY_PORT=$3
export DIR_SERVICE_HOST=$4
export OBJECT_DIR=$5
export UUID=$6
export PHY_IP=$7

IPADDR=$(hostname -I)
HOSTNAME=$(hostname)
LOGS_FILE=/var/log/huoyin/xtreemfs/

envsubst < /etc/xos/xtreemfs/osdconfig.properties.template > /etc/xos/xtreemfs/osdconfig.properties

echo "acl.port = $PROXY_PORT" > /etc/xos/xtreemfs/proxy.conf

REPLICAS=$8
DIR_SERVICE_HOST_2=$9
DIR_SERVICE_HOST_3=$10

if [ $REPLICAS = YES ] ; then
   sed -i "s@^#dir_service1.host.*@dir_service1.host = ${DIR_SERVICE_HOST_2}@" /etc/xos/xtreemfs/osdconfig.properties
   sed -i "s@^#dir_service2.host.*@dir_service1.host = ${DIR_SERVICE_HOST_3}@" /etc/xos/xtreemfs/osdconfig.properties
   sed -i "s@^#dir_service1.port@dir_service1.port@" /etc/xos/xtreemfs/osdconfig.properties
   sed -i "s@^#dir_service2.port@dir_service2.port@" /etc/xos/xtreemfs/osdconfig.properties
fi
   
mkdir $OBJECT_DIR -p
mkdir $LOGS_FILE -p

cat /etc/hosts | grep $IPADDR
if [ $? != 0 ] ; then
    echo "$IPADDR $HOSTNAME" >> /etc/hosts
fi

chown -R xtreemfs:xtreemfs $OBJECT_DIR

sh /usr/java/beiyun/snmp_proxy/start_snmp_proxy.sh

su -s /bin/bash xtreemfs -c "/usr/bin/java -ea -cp /usr/share/java/xtreemfs.jar:/usr/share/java/jdmkrt.jar:/usr/share/java/jdmktk.jar:/usr/share/java/commons-codec-1.3.jar org.xtreemfs.osd.OSD  /etc/xos/xtreemfs/osdconfig.properties" | tee ${LOGS_FILE}/xsfs-osd-${LISTEN_PORT}-${HTTP_PORT}.log
