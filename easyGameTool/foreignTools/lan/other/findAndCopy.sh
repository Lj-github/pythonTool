#!/bin/sh

# 英文版地址
english_dir=/Users/admin/Documents/ljworkspace/local/cocos/project/Pikachu/
russion_dir=/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_english/

if [ ! -n "$1" ] ;then
    echo "没有输入任何参数!\n请输入'文件路径'"
else
    echo "输入的参数是$1,将会拷贝所有的$1文件"
    filename="$1""*"
    fileArray=$(find "${english_dir}" -type f -name "${filename}" -not -iname "*.js" -not -iname "*.map" -not -iname "*.coffee")
    #cd "$english_dir"
    #find . -type f -name "${filename}" -not -iname "*.js" -not -iname "*.map" -not -iname "*.coffee" -exec mkdir -p 'dirname /Users/songbin/clientprojects/pikachu_english/{}' ';'
    #find . -type f -name "${filename}" -not -iname "*.js" -not -iname "*.map" -not -iname "*.coffee" -exec cp -v '{}' '/Users/songbin/clientprojects/pikachu_english/{}' ';'
    echo "$fileArray"

    for file in ${fileArray}
    do
        echo "search file $file"
        if [ -f "$file" ]; then
            newfilePth="${file%/*}"
            mkdir -p newfilePth
            echo "$file searched"
            /Users/admin/Documents/ljworkspace/local/cocos/project/foreignTools/cpOneToOne.sh "$file"
        fi
    done
fi



