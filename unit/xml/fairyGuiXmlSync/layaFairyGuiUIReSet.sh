#!/usr/bin/env bash
echo "开始执行"
SHELL_FOLDER=$(dirname "$0")
ds=`pwd`
echo $SHELL_FOLDER
python3 ${SHELL_FOLDER}'/'main.py
echo "执行完毕"