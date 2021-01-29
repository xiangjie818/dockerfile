#!/bin/bash
chown -R root:xtreemfs /etc/xos/xtreemfs
chown -R xtreemfs:root /var/lib/xtreemfs
while true
do
    su -s /bin/bash xtreemfs -c "/usr/bin/java -ea -cp /usr/share/java/xtreemfs.jar:/usr/share/java/jdmkrt.jar:/usr/share/java/jdmktk.jar:/usr/share/java/commons-codec-1.3.jar org.xtreemfs.dir.DIR  /etc/xos/xtreemfs/dirconfig.properties"
    sleep 30
done
