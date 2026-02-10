#!/bin/sh

# 日志函数
log() {
    logger -t "campus_login" "$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1"
}

# URL配置
LOGIN_URL="http://172.16.200.101/eportal/InterFace.do?method=login"
CHECK_URL="http://172.16.200.101/eportal/InterFace.do?method=getOnlineUserInfo"

# 用户配置
USER_INDEX="抓包获取的 userIndex"
USER_ID="你的学号"
PASSWORD="抓包获取的加密密码"
QUERY_STRING="抓包获取，格式: wlanuserip=xxx&wlanacname=xxx&ssid=&nasip=xxx&..."

# 检查在线状态
check_status() {
    local response
    response=$(curl -s -X POST "$CHECK_URL" \
        -H "Accept: */*" \
        -H "Content-Type: application/x-www-form-urlencoded; charset=UTF-8" \
        -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)" \
        -H "Origin: http://172.16.200.101" \
        -d "userIndex=$USER_INDEX" \
        --connect-timeout 10)
    
    echo "$response" | grep -q '"result":"success"'
    return $?
}

# 执行登录
do_login() {
    local response
    response=$(curl -s -X POST "$LOGIN_URL" \
        -H "Accept: */*" \
        -H "Content-Type: application/x-www-form-urlencoded; charset=UTF-8" \
        -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)" \
        -H "Origin: http://172.16.200.101" \
        -d "userId=$USER_ID" \
        -d "password=$PASSWORD" \
        -d "service=" \
        -d "queryString=$QUERY_STRING" \
        -d "operatorPwd=" \
        -d "operatorUserId=" \
        -d "validcode=" \
        -d "passwordEncrypt=true" \
        -d "userIndex=$USER_INDEX" \
        --connect-timeout 10)
    
    if echo "$response" | grep -q '"result":"success"'; then
        log "登录成功"
        return 0
    else
        log "登录失败"
        return 1
    fi
}

# 主循环
main() {
    log "校园网自动登录脚本启动"
    
    while true; do
        if ! check_status; then
            log "检测到掉线，尝试重新登录"
            do_login
            sleep 5
        else
            log "当前在线"
        fi
        
        # 随机等待30-60秒
        sleep $(awk 'BEGIN{srand();print int(rand()*(31)+30)}')
    done
}

# 启动主程序
main 