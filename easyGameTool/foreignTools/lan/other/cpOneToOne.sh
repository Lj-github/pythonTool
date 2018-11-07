#!/bin/sh

# 皮卡丘客户端地址
if [ ! -n "$1" ] ;then
    echo "没有输入任何参数!\n请输入'文件路径'"
else
    echo "输入的参数是$1,将会拷贝所有的$1文件"
    replaceStr_a="Pikachu"
    replaceStr_b="pikachu_english"
    firstStr="$1"
    file2="${firstStr/Pikachu/pikachu_english}"
    echo "拷贝到 $file2"
    newfilePth="${file2%/*}"
    mkdir -p "$newfilePth"
    echo "创建文件夹 $newfilePth"
    newfilePth1="${newfilePth%/*}"
    tpsname="*.tps"
    filetpsPth="${newfilePth1/pikachu_english/Pikachu}"
    echo "查找tps 文件 ${filetpsPth}"

    fileArray=$(find "${filetpsPth}" -type f -name "${tpsname}")
    for file in ${fileArray}
    do
    if [ -f "$file" ]; then
        echo "创建文件tps $file"
        file3="${file/Pikachu/pikachu_english}"
        cp -rf "${file}" "$file3"
    fi
    done
    cp -rf "$1" "${file2}"
fi



