# version = 0.0.5

try:
    import socket
    import requests
    import time
    from colorama import Fore, Back, Style
except ModuleNotFoundError:
    print('本机缺少必要依赖，请查看帮助文件解决问题')
    input()
    exit()


def log(type: str, content: str):
    time_now = time.strftime(r'%H:%M:%S', time.localtime())
    if type == 'normal':
        print('[%s][Client] %s' % (time_now, content))
    elif type == 'warning':
        print(Fore.RED + '[%s][Client] %s' % (time_now, content) + Fore.RESET)
    elif type == 'server':
        print(Fore.GREEN + '[%s][Server] %s' % (time_now, content) +
              Fore.RESET)


def pinput(content):
    time_now = time.strftime(r'%H:%M:%S', time.localtime())
    a = input(Fore.BLUE + '[%s][Client] %s >>> ' % (time_now, content) +
              Fore.RESET)
    return a


ip = socket.gethostbyname(socket.gethostname())
log('normal', '本机ip为 %s' % (ip))
aim_ip = pinput('请输入服务器ip(不知道可以留空)')
if aim_ip == '':
    ip = ip.split('.')
    ip[-1] = '137'
    ip_ = ''
    for i in ip:
        ip_ += i+'.'
    ip_ = ip_[:-1]
    aim_ip = 'http://' + ip_ + ':5000'
else:
    aim_ip = 'http://' + aim_ip + ':5000'
log('normal', '服务器ip %s' % (aim_ip))
log('normal', '尝试与服务器取得联系...')
try:
    response = requests.get('%s' % (aim_ip), timeout=5)
except requests.exceptions.Timeout:
    log('warning', '服务器响应超时，可能是因为服务器未启动或防火墙设置')
    exit()
log('server', '连接成功')
log('server', response.text)
log('normal', '现在你可以进行如下操作：')
while True:
    for i in [
            '1. 向服务器发送信息', '2. 抽卡1次', '3. 抽卡10次', '4. 获取所有人的抽卡记录（5星）',
            '5. 重置抽卡记录', '6. 退出'
    ]:
        log('normal', i)
    choice = pinput('请选择你要进行哪项操作（输入序号）')
    if choice == '1':
        send = pinput('请输入')
        try:
            requests.post(aim_ip + '/talk', data={'ip': ip, 'content': send})
        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            log('warning', '服务器响应超时，可能是因为服务器未启动或防火墙设置')
            exit()
    elif choice == '2':
        try:
            post = requests.post(aim_ip + '/wish',
                                 data={
                                     'ip': ip,
                                     'times': 1
                                 })
        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            log('warning', '服务器响应超时，可能是因为服务器未启动或防火墙设置')
            exit()
        code = post.status_code
        if code == 200 or code == 201 or code == 202:
            result = post.json()
            log(
                'server',
                '你获得了%s星%s' % (str(result['message']['result'][0]['star']),
                               str(result['message']['result'][0]['name'])))
            log(
                'server', '已垫%s抽，距离上次出紫已有%s抽' %
                (str(result['message']['g']), str(result['message']['p'])))
        elif code == 429:
            log('server', '请求频率过高，请尝试降低频率')
    elif choice == '3':
        try:
            post = requests.post(aim_ip + '/wish',
                                 data={
                                     'ip': ip,
                                     'times': 10
                                 })
        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            log('warning', '服务器响应超时，可能是因为服务器未启动或防火墙设置')
            exit()
        code = post.status_code
        if code == 200 or code == 201 or code == 202:
            result = post.json()
            for i in range(10):
                log(
                    'server',
                    '你获得了%s星%s' % (str(result['message']['result'][i]['star']),
                                   str(result['message']['result'][i]['name'])))
            log(
                'server', '已垫%s抽，距离上次出紫已有%s抽' %
                (str(result['message']['g']), str(result['message']['p'])))
        elif code == 429:
            log('server', '请求频率过高，请尝试降低频率')

    elif choice == '4':
        try:
            post = requests.post(aim_ip + '/list')
        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            log('warning', '服务器响应超时，可能是因为服务器未启动或防火墙设置')
            exit()
        code = post.status_code
        if code == 200 or code == 201 or code == 202:
            result = post.json()
            if 'notice' in result['message'].keys():
                log('server', 'No one wished')
            else:
                for i in result['message'].keys():
                    for j in result['message'][i]:
                        log('server', "%s花费了%s抽获得了%s" %
                            (i, j['paid'], j['name']))
        elif code == 429:
            log('server', '请求频率过高，请尝试降低频率')

    elif choice == '5':
        try:
            post = requests.post(aim_ip + '/reset', data={'ip': ip})
        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            log('warning', '服务器响应超时，可能是因为服务器未启动或防火墙设置')
            exit()
        code = post.status_code
        if code == 200 or code == 201 or code == 202:
            result = post.json()
            log('server', result['message'])
        elif code == 429:
            log('server', '请求频率过高，请尝试降低频率')

    elif choice == '6':
        try:
            requests.post(aim_ip + '/quit', data={'ip': ip})
            break
        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            log('warning', '服务器响应超时，可能是因为服务器未启动或防火墙设置')

log('warning', '成功断开了连接')
input('按Enter键退出程序')
