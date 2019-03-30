#!/usr/bin/env bash
#起动 所有 project flask 项目

echo "开始启动 Jenkins"
sh /Users/admin/Documents/environment/apache-tomcat/bin/shutdown.sh
sleep 5
sh /Users/admin/Documents/environment/apache-tomcat/bin/startup.sh
echo "Jenkins 起动成功"
# http://192.168.1.214:8080/loginError


#jenkens /Users/admin/Documents/environment/apache-tomcat/bin/catalina.sh run

#http://192.168.1.214:8888/jenkins/

