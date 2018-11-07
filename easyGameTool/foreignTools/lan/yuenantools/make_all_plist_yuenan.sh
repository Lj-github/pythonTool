#!/bin/sh
for file in `find /Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english/tools/pikachuFontAndPlist/bin -type f -name "*.sh"`;do
    echo $file
    sh $file
done