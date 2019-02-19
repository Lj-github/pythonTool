#!/usr/bin/env bash
# 备份  mysqldump -d pkc_webdata playerloginzhenghe -uroot >daily_player_2019_01_25_t.sql #表 结构
#mysqldump -t pkc_webdata playerloginzhenghe -uroot >daily_player_2019_01_25.sql 数据
# 备份  mysqldump -d pkc_webdata playerorderzhenghe -uroot >playerorderzhenghe_t.sql #表 结构
#mysqldump -t pkc_webdata playerorderzhenghe -uroot >playerorderzhenghe.sql 数据

#dump  表 + 数据  mysqldump -h10.0.4.46 -ugame -perdossol pkc_log189 create_player_log_2019_02_19 > log.sql


#scp -P 2202 pikachuadmin@mini-gm.easygametime.com:/home/pikachuadmin/playerloginzhenghe_t.sql /Users/admin/Desktop/
#scp -P 2202 pikachuadmin@mini-gm.easygametime.com:/home/pikachuadmin/playerloginzhenghe.sql /Users/admin/Desktop/
scp -P 2202 pikachuadmin@mini-gm.easygametime.com:/home/pikachuadmin/log.sql /Users/admin/Desktop/
scp -P 2202 pikachuadmin@mini-gm.easygametime.com:/home/pikachuadmin/daily_player_2019_01_25.sql /Users/admin/Desktop/