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
    aim_ip = 'http://' + ip[:11] + '37:5000'
    log('normal', '尝试拼装服务器ip %s' % (aim_ip))
else:
    aim_ip = 'http://' + aim_ip + ':5000'
    log('normal', '服务器ip %s' % (aim_ip))

log('normal', '尝试与服务器取得联系...')
try:
    response = requests.get('%s' % (aim_ip), timeout=5)
except requests.exceptions.Timeout:
    log('warning', '服务器响应超时，可能是因为服务器未启动或防火墙设置')
    exit()
log('normal', '连接成功')
log('server', response.text)
log('normal', '现在你可以进行如下操作：')
while True:
    for i in [
            '1. 向服务器发送信息', '2. 抽卡1次', '3. 抽卡10次', '4. 获取抽卡排行榜', '5. 重置抽卡记录',
            '6. 退出'
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
            result = requests.post(aim_ip + '/wish',
                                   data={
                                       'ip': ip,
                                       'times': 1
                                   }).json()
        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            log('warning', '服务器响应超时，可能是因为服务器未启动或防火墙设置')
            exit()
        log(
            'server', '你获得了%s星%s' % (str(result['result'][0]['star']),
                                     str(result['result'][0]['name'])))
        log('server',
            '已垫%s抽，距离上次出紫已有%s抽' % (str(result['g']), str(result['p'])))
    elif choice == '3':
        try:
            result = requests.post(aim_ip + '/wish',
                                   data={
                                       'ip': ip,
                                       'times': 10
                                   }).json()
        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            log('warning', '服务器响应超时，可能是因为服务器未启动或防火墙设置')
            exit()
        for i in range(10):
            log(
                'server', '你获得了%s星%s' % (str(result['result'][i]['star']),
                                         str(result['result'][i]['name'])))
        log('server',
            '已垫%s抽，距离上次出紫已有%s抽' % (str(result['g']), str(result['p'])))
    elif choice == '4':
        try:
            result = requests.post(aim_ip + '/list').json()
        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            log('warning', '服务器响应超时，可能是因为服务器未启动或防火墙设置')
            exit()
        if 'notice' in result.keys():
            log('server', 'No one wished')
        else:
            for i in result.keys():
                for j in result[i]:
                    log('server', "%s花费了%s抽获得了%s" % (i, j['paid'], j['name']))
    elif choice == '5':
        try:
            result = requests.post(aim_ip + '/reset', data={'ip': ip})
        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            log('warning', '服务器响应超时，可能是因为服务器未启动或防火墙设置')
            exit()
        log('server', 'Reset succesfully!')
    elif choice == '6':
        try:
            requests.post(aim_ip + '/quit', data={'ip': ip})
            break
        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            log('warning', '服务器响应超时，可能是因为服务器未启动或防火墙设置')

log('warning', '成功断开了连接')
input('按Enter键退出程序')
