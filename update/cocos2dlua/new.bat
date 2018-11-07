@echo off

echo PyThon 
::下面是批处理代码

cd script
readfile.py

::暂停 3 秒时间
ping -n 3 127.0.0.1 > nul

::暂停
::pause
Exit