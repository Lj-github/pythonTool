
rm -rf /d/work/easygame/client/SmartPikachu/SmartpikachuGame/dataBake/
mkdir -p /d/work/easygame/client/SmartPikachu/SmartpikachuGame/dataBake/



find /d/work/easygame/svn/aiweiyou_pokmon/pokmon_weixin/tools/exceltojson/json -iname '*.*' -exec cp \{\} /d/work/easygame/client/SmartPikachu/SmartpikachuGame/dataBake/ \;



svnPath=/d/work/easygame/svn/aiweiyou_pokmon/pokmon_weixin
jsonPath=$svnPath/tools/exceltojson/json
descPath=$svnPath/tools/exceltojson/ts
appPath=/d/work/easygame/client/SmartPikachu/SmartpikachuGame/

svn update $svnPath
rm $appPath/dataBake/*.json
cp  $jsonPath/*.json $appPath/dataBake/
cp  $jsonPath/*Group.json $appPath/resource/data/
echo 'copy desc files'
cp $descPath/* $appPath/libs/

sh /d/work/easygame/client/SmartPikachu/other/resRepend/resDepend.sh