FROM xtfs-common:1.6.0-alpine
  
MAINTAINER zhaoxiangjie

ENV DIR_SERVICE_HOST=192.168.0.14
ENV HOSTNAME=node1.test.com
#CMD ["/usr/bin/java", "-ea", \
#     "-cp", "/usr/share/java/xtreemfs.jar:/usr/share/java/jdmkrt.jar:/usr/share/java/jdmktk.jar:/usr/share/java/commons-codec-1.3.jar", \
#     "org.xtreemfs.mrc.MRC", "/etc/xos/xtreemfs/mrcconfig.properties"]
COPY start-mrc.sh /
CMD sh /start-mrc.sh
