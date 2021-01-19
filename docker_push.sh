#!/bin/bash
ARCH=$(arch)
if [ $ARCH = x86_64 ] ; then
    arch=amd64
elif [ $ARCH = aarch64 ] ; then
    arch=arm64
else
    echo "Unsupported system architecture"
fi

#repo_dest=swr.cn-north-1.myhuaweicloud.com/xtfs
repo_dest=registry.cn-beijing.aliyuncs.com/xtreemfs
#docker login -u cn-north-1@Q35W0RM021TWJYKWBW0B -p 116e06d41e8d48c2ef18c72d39eec7b53a4cffde0f7c41ef78a99c7463edeaf4 swr.cn-north-1.myhuaweicloud.com
# docker login --username=xiangjie818@163.com registry.cn-beijing.aliyuncs.com

img=$1
img_tag=$(docker images | grep ${img} | awk '{print $2}')

for i in $img_tag ; do
    docker tag ${img}:${i} ${repo_dest}/${img}:${i}-${arch}
    docker push ${repo_dest}/${img}:${i}-${arch}
    docker rmi ${repo_dest}/${img}:${i}-${arch}
done
