path=$1
if [ -z "${path}" ]
then
echo "请输入exml文件的路径"
else
jsPath='/Users/admin/Documents/ljworkspace/local/egret/SmartPikachu/SmartPikachuGit/SmartPikachu/other/exmlTest/'
cd $jsPath
node $jsPath/exmlTest.js $path
cat $jsPath/output/varDefine.txt
fi
