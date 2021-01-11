#!/bin/bash
repo_dest=swr.cn-north-1.myhuaweicloud.com/xtfs
docker login -u cn-north-1@Q35W0RM021TWJYKWBW0B -p 116e06d41e8d48c2ef18c72d39eec7b53a4cffde0f7c41ef78a99c7463edeaf4 swr.cn-north-1.myhuaweicloud.com

img=$1
img_tag=$(docker images | grep ${img} | awk '{print $2}')

docker tag ${img}:${img_tag} ${repo_dest}/${img}:${img_tag}
docker push ${repo_dest}/${img}:${img_tag}
docker rmi ${repo_dest}/${img}:${img_tag}
