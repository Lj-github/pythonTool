#!/bin/sh

# 英文版地址
project_dir=/Users/admin/Documents/ljworkspace/local/cocos/project/pikachu_englishGit/pikachu_english/
src_dir1=/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/翻译美术图
src_dir=/Users/admin/Documents/ljworkspace/local/cocos/assets/pikachu/sanguo/art_pikachu/绿洲/

function read_dir(){
    for file in $(ls $1)
    do
        if [ -d $1"/"$file ];  #注意此处之间一定要加上空格，否则会报错
        then
            read_dir $1"/"$file
        else
            echo $1"/"$file
            filename="${file##*/}"
            fileArray=$(find "${project_dir}" -type f -name "${filename}" -not -iname "*.js" -not -iname "*.txt" -not -iname "*.map" -not -iname "*.coffee")
            # echo "find fileArray $fileArray"
            for file1 in ${fileArray}
            do
                # echo "search file $file1"
                if [ -f "$file1" ]; then
                    cp -p $1"/"$file "${file1}"
                fi
            done

        fi
    done
}
read_dir $src_dir1
read_dir $src_dir




