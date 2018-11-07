
svnpath="/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/aiweiyou_pokmon/pokmon_weixin/tools/微信/"
protocolOutPath="/Users/admin/Documents/ljworkspace/local/egret/SmartPikachu/SmartPikachuGit/SmartPikachu/SmartpikachuGame/libs/ezModules/gameProtocol"
resourcePath="/Users/admin/Documents/ljworkspace/local/egret/SmartPikachu/SmartPikachuGit/SmartPikachu/SmartpikachuGame/resource/data/"
echo "更新svn"
svn update $svnpath
echo "svn 更新完毕"
# 
# resPth=${protocolOutPath}/../../../resource/data/
cp $svnpath*msgData.json $resourcePath
#cp $svnpath*GameProtocol.js $protocolOutPath/bin/
cp $svnpath/*.ts $protocolOutPath/libs/