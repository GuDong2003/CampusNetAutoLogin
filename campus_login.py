#!/usr/bin/env python3
import requests
import time
import random
import logging
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/var/log/campus_login.log')
    ]
)

# 配置信息
header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '866',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': '172.16.200.101',
    'Origin': 'http://172.16.200.101',
    'Referer': '# 抓包获取，参考模板文件',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
}

dataLogin = {
    'userId': '你的学号',
    'password': '抓包获取的加密密码',
    'service': '',
    'queryString': '抓包获取，格式: wlanuserip=xxx&wlanacname=xxx&ssid=&nasip=xxx&...',
    'operatorPwd': '',
    'operatorUserId': '',
    'validcode': '',
    'passwordEncrypt': 'true',
    'userIndex': '抓包获取的 userIndex'
}

dataCheck = {
    'userIndex': '抓包获取的 userIndex'
}

loginUrl = 'http://172.16.200.101/eportal/InterFace.do?method=login'
checkStatusUrl = 'http://172.16.200.101/eportal/InterFace.do?method=getOnlineUserInfo'

def check_and_login():
    try:
        # 检查在线状态
        response = requests.post(url=checkStatusUrl, headers=header, data=dataCheck, timeout=10)
        response.encoding = 'utf-8'
        content = response.text.encode().decode("unicode_escape").encode('raw_unicode_escape').decode()
        status_index = content.find('"result":"')

        # 根据状态执行操作
        if content[status_index + 10:status_index + 14] == 'wait' or content[status_index + 10:status_index + 17] == 'success':
            logging.info("当前处于在线状态")
        else:
            logging.warning("当前已经下线，正在尝试登录！")
            # 尝试登录
            login_response = requests.post(url=loginUrl, headers=header, data=dataLogin, timeout=10)
            login_response.encoding = 'utf-8'
            login_content = login_response.text.encode().decode("unicode_escape").encode('raw_unicode_escape').decode()
            result_index = login_content.find('"result":"')

            # 检查登录结果
            if login_content[result_index + 10:result_index + 17] == 'success':
                logging.info("登录成功！")
            else:
                logging.error("登录失败！")

    except Exception as e:
        logging.error(f"监测出错，请检查网络是否连通: {str(e)}")

def main():
    logging.info("校园网自动登录服务启动")
    while True:
        try:
            check_and_login()
            time.sleep(random.randint(5, 20))
        except Exception as e:
            logging.error(f"发生错误: {str(e)}")
            time.sleep(1)

if __name__ == "__main__":
    main()
