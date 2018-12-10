#!/usr/bin/env bash
path=$1
if [ -z "${path}" ]
then
echo "请输入exml文件的路径"
else
jsPath='D:\work\easygame\client\SmartPikachu\other\exmlTest'
cd $jsPath
node $jsPath/exmlTest.js $path
cat $jsPath/output/varDefine.txt
fi
