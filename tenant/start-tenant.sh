#!/bin/bash
java -jar -Dspring.datasource.url="jdbc:mysql://${mysql_host}:3306/beiyun?useUnicode=true&useSSL=false&characterEncoding=UTF-8&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&serverTimezone=${timezone}" -Dspring.datasource.username=${mysql_user} -Dspring.datasource.password=${mysql_pass} /usr/java/beiyun/beiyun-1.0_Beta.jar --spring.profiles.active=test --kafka.bootstrap-servers=${kafka_host}:${kafka_port} --pki.server.url=http://${pki_host}:{pki_port}/ --volume.server.url=http://${volume_host}:${volume_port} --xtreemfs.DIR.host=${dir_host} --xtreemfs.DIR.host_ip=${dir_host} --spring.elasticsearch.url=${elasticsearch_host} --file.share_url=http://${file_share_host}:8200 | tee ${logs_dir}/beiyun.log