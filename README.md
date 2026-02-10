# CampusNetAutoLogin

校园网自动登录工具，适用于使用 ePortal 认证系统的校园网络。自动检测网络连接状态，断线后自动重新认证，保持持续在线。

本工具参考 `https://github.com/Gloridust/RuijieWIFI-AutoLogin`

现已毕业，刚好闲来无事，故将代码发出来

主要用于郑州西亚斯学院的锐捷校园网认证，亲测可用

学弟学妹们看到了可以试试

## 功能特性

- 定时检测校园网在线状态
- 断线自动重连
- 随机检测间隔，避免被识别为异常流量
- 支持日志记录（控制台 + 文件）
- 提供 Python / Shell / 编译二进制 三种运行方式

## 项目结构

```
.
├── campus_login.py                    # Python 主脚本（带日志）
├── python/
│   ├── CampusNetAutoLogin.py          # Python 简洁版
│   ├── CampusNetAutoLogin.sh          # Shell 版本
│   ├── CampusNetAutoLogin.spec        # PyInstaller 打包配置
│   └── CampusNetAutoLogin_内容需要修改.py  # 配置模板
```

## 使用前准备

使用前需要通过**抓包**获取你自己的认证参数。

### 抓包步骤

1. 电脑连接校园 Wi-Fi，浏览器会自动跳转到认证页面（如果没有跳转，访问任意 HTTP 网站即可）
2. 按 **F12** 打开浏览器开发者工具，切换到 **Network（网络）** 面板
3. 勾选 **Preserve log（保留日志）**，以免页面跳转后请求记录丢失
4. 在认证页面输入你的学号和密码，点击登录
5. 在 Network 面板中找到 `InterFace.do?method=login` 这个 POST 请求
6. 点击该请求，查看以下信息：

### 从请求头（Request Headers）中获取

| 参数 | 在哪里找 | 说明 |
|------|----------|------|
| `Referer` | Request Headers → Referer | 一串很长的 URL，包含 `wlanuserip`、`mac` 等参数 |

### 从请求体（Form Data / Payload）中获取

| 参数 | 在哪里找 | 说明 |
|------|----------|------|
| `userId` | Form Data → userId | 你的学号 |
| `password` | Form Data → password | **加密后的密码**（一串十六进制字符，不是你的明文密码） |
| `queryString` | Form Data → queryString | 包含 `wlanuserip=xxx&wlanacname=xxx&mac=xxx&...` 的字符串 |
| `userIndex` | Form Data → userIndex | 一串十六进制字符，用于标识你的会话 |

### 填入配置

将上述参数填入脚本中对应位置。可以参考 `python/CampusNetAutoLogin_内容需要修改.py` 模板文件，其中标注了每个字段的填写位置。

> **提示**：`queryString`、`userIndex` 和 `Referer` 中的值可能会在重新连接 Wi-Fi 后发生变化，届时需要重新抓包获取。

## 运行方式

### Python 脚本

```bash
# 安装依赖
pip install requests

# 运行（简洁版）
python3 python/CampusNetAutoLogin.py

# 运行（带日志版）
python3 campus_login.py
```

### Shell 脚本

```bash
chmod +x python/CampusNetAutoLogin.sh
./python/CampusNetAutoLogin.sh
```

### 编译为独立可执行文件

```bash
pip install pyinstaller
cd python
pyinstaller CampusNetAutoLogin.spec
# 生成的文件在 dist/CampusNetAutoLogin
```

## 后台运行（macOS / Linux）

```bash
# 使用 nohup 后台运行
nohup python3 campus_login.py &

# 或使用 screen
screen -S campus
python3 campus_login.py
# Ctrl+A, D 分离会话
```

## 工作原理

```
启动 → 检查在线状态(getOnlineUserInfo)
         ├── result: success/wait → 在线，等待后再次检查
         └── 其他 → 已断线 → 发送登录请求(login)
                                ├── 成功 → 等待后继续检查
                                └── 失败 → 记录错误，继续重试
```

## 注意事项

- 密码字段是**加密后的值**，不是明文密码，需要从抓包中获取
- `queryString` 和 `userIndex` 等参数可能会在重新连接 Wi-Fi 后变化，需要重新抓包
- 请勿将包含个人凭据的配置文件提交到公开仓库
- 本工具仅供个人学习使用

## 依赖

- Python 3.6+
- [requests](https://pypi.org/project/requests/)

## License

MIT
