#!/bin/bash

#pip3 list
pypi_mirror=https://mirrors.aliyun.com/pypi/simple

if [ ! "x$pypi_mirror" = "x" ];then
    mirror_param="-i $pypi_mirror"
fi

echo pip3 install $mirror_param pip --upgrade
pip3 install $mirror_param setuptools --upgrade
pip3 install $mirror_param wheel
pip3 install $mirror_param cffi
pip3 install $mirror_param pycparser
pip3 install $mirror_param -r requirement.txt

pip3 list
