#!/bin/bash
image_name=$1

docker build -t $1 .
