import requests
import time
import random

# 配置信息
header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '866',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 非必要请勿启用
    # 'Cookie': '',
    'Host': '172.16.200.101',
    'Origin': 'http://172.16.200.101',
    'Referer': '！！！修改 抓包里面可以找到！！！',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
}

dataLogin = {
    'userId': '！！！学号！！！',
    'password': '！！！这是加密的密码，在抓包里面找！！！',
    'service': '',
    'queryString': '！！！参考 找对应字段  wlanuserip=1234&wlanacname=1234&ssid=&nasip=1234&snmpagentip=&mac=123&t=wireless-v2&url=123&apmac=&nasid=123&vid=123&port=123&nasportid=123！！！',
    'operatorPwd': '',
    'operatorUserId': '',
    'validcode': '',
    'passwordEncrypt': 'true',
    'userIndex': '！！！抓包里面有！！！'
}

dataCheck = {
    'userIndex': '！！！抓包里面有！！！'
}

loginUrl = 'http://172.16.200.101/eportal/InterFace.do?method=login'
checkStatusUrl = 'http://172.16.200.101/eportal/InterFace.do?method=getOnlineUserInfo'

def check_and_login():
    # 检查在线状态
    response = requests.post(url=checkStatusUrl, headers=header, data=dataCheck)
    response.encoding = 'utf-8'
    content = response.text.encode().decode("unicode_escape").encode('raw_unicode_escape').decode()
    status_index = content.find('"result":"')

    # 根据状态执行操作
    if content[status_index + 10:status_index + 14] == 'wait' or content[status_index + 10:status_index + 17] == 'success':
        print(time.asctime(time.localtime(time.time())), "当前处于在线状态。")
    else:
        print(time.asctime(time.localtime(time.time())), "当前已经下线，正在尝试登录！")
        # 尝试登录
        login_response = requests.post(url=loginUrl, headers=header, data=dataLogin)
        login_response.encoding = 'utf-8'
        login_content = login_response.text.encode().decode("unicode_escape").encode('raw_unicode_escape').decode()
        result_index = login_content.find('"result":"')

        # 检查登录结果
        if login_content[result_index + 10:result_index + 17] == 'success':
            print(time.asctime(time.localtime(time.time())), "登录成功！")

while True:
    try:
        check_and_login()
    except Exception as e:
        print(time.asctime(time.localtime(time.time())), "监测出错，请检查网络是否连通。", str(e))
        time.sleep(1)
        continue
    time.sleep(random.randint(1, 3))