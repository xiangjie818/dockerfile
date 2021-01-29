#!/bin/bash
sed -i "s@dir_service.host =.*@dir_service.host = $DIR_SERVICE_HOST@g" /etc/xos/xtreemfs/mrcconfig.properties
sed -i "s@# hostname = .*@hostname = ${HOSTNAME}@g" /etc/xos/xtreemfs/mrcconfig.properties
chown -R root:xtreemfs /etc/xos/xtreemfs
chown -R xtreemfs:root /var/lib/xtreemfs

while true
do
    su -s /bin/bash xtreemfs -c "/usr/bin/java -ea -cp /usr/share/java/xtreemfs.jar:/usr/share/java/jdmkrt.jar:/usr/share/java/jdmktk.jar:/usr/share/java/commons-codec-1.3.jar org.xtreemfs.mrc.MRC  /etc/xos/xtreemfs/mrcconfig.properties"
    sleep 30
done
