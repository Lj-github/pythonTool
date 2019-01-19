#!/usr/bin/env bash
# 备份  mysqldump -d pkc_webdata playerloginzhenghe -uroot >playerloginzhenghe_t.sql #表 结构
#mysqldump -t pkc_webdata playerloginzhenghe -uroot >playerloginzhenghe.sql 数据
# 备份  mysqldump -d pkc_webdata playerorderzhenghe -uroot >playerorderzhenghe_t.sql #表 结构
#mysqldump -t pkc_webdata playerorderzhenghe -uroot >playerorderzhenghe.sql 数据

#scp -P 2202 pikachuadmin@mini-gm.easygametime.com:/home/pikachuadmin/playerloginzhenghe_t.sql /Users/admin/Desktop/
#scp -P 2202 pikachuadmin@mini-gm.easygametime.com:/home/pikachuadmin/playerloginzhenghe.sql /Users/admin/Desktop/
scp -P 2202 pikachuadmin@mini-gm.easygametime.com:/home/pikachuadmin/playerorderzhenghe_t.sql /Users/admin/Desktop/
scp -P 2202 pikachuadmin@mini-gm.easygametime.com:/home/pikachuadmin/playerorderzhenghe.sql /Users/admin/Desktop/