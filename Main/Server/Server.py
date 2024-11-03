# version = 0.0.5

import random
from colorama import Fore
from flask import Flask, request, render_template, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pathlib import Path
import json
import socket

app = Flask(__name__)
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=[
    "30 per minute", "1/seconds"]
)

bc = [
    "冷刃", "黎明神剑", "飞天御剑", "铁影阔剑", "沐浴龙血的剑", "以理服人", "黑缨枪", "魔导绪论", "讨龙英杰谭",
    "翡玉法球", "鸦羽弓", "神射手之誓", "弹弓"
]
pc = [
    "弓藏", "祭礼弓", "绝弦", "昭心", "祭礼残章", "流浪乐章", "匣里灭辰", "雨裁", "祭礼大剑", "钟剑",
    "匣里龙吟", "祭礼剑", "笛剑", "西风剑", "西风大剑", "西风长枪", "西风秘典", "西风猎弓", "嘉明", "夏沃蕾",
    "夏洛蒂", "菲米尼", "琳妮特", "绮良良", "卡维", "米卡", "瑶瑶", "珐露珊", "莱依拉", "坎蒂丝", "多莉",
    "柯莱", "鹿野院平藏", "久岐忍", "云堇", "五郎", "托马", "九条裟罗", "早柚", "烟绯", "罗莎莉亚", "辛焱",
    "迪奥娜", "诺艾尔", "菲谢尔", "丽莎", "凯亚", "雷泽", "重云", "凝光", "砂糖", "芭芭拉", "安柏", "香菱",
    "班尼特", "行秋", "北斗"
]
gc = [
    "琴", "莫娜", "刻晴", "七七", "迪卢克", "提纳里", "迪希雅", "天空之翼", "天空之卷", "天空之脊", "天空之傲",
    "天空之刃", "阿莫斯之弓", "四风原典", "和璞鸢", "狼的末路", "风鹰剑"
]
local_ip = socket.gethostbyname(socket.gethostname())


def message(status, code, content):
    a = {'status': status, 'code': code, 'message': content}
    return a


@limiter.exempt
@app.route('/')
def index():
    return 'Connected Successfully! 现在你可以通过访问 http://%s:5000/index 来实现课堂摸鱼（可以看视频）' % (local_ip), 200


@limiter.exempt
@app.route('/index')
def show():
    return render_template("index.html")


@limiter.exempt
@app.route('/404.html')
def error():
    return render_template("404.html")


@limiter.exempt
@app.route('/help.html')
def help_():
    return render_template("help.html")


@limiter.exempt
@app.route('/video')
def video_JiYan():
    if request.method == 'GET':
        videoname = request.args.get('name')
    return render_template('main.html', movie='static/videos/%s.mp4' % (videoname))


@app.route('/wish', methods=['GET', 'POST'])
def wish():
    ip = request.form.get('ip')
    times = request.form.get('times')
    path = Path('./Data/%s.json' % (ip))
    dictionary = {}
    if path.exists():
        contents = path.read_text()
        dictionary = json.loads(contents)
    else:
        dictionary = {'ip': ip, 'gold': 0, 'purple': 0, 'paid': []}
        contents = json.dumps(dictionary,
                              sort_keys=True,
                              indent=4,
                              separators=(',', ':'))
        path.write_text(contents)

    everyone_path = Path('./Data/everyone.json')
    everyone_dict = {}
    if everyone_path.exists():
        contents = everyone_path.read_text()
        everyone_dict = json.loads(contents)
        if ip not in everyone_dict.keys():
            everyone_dict[ip] = []
    else:
        everyone_dict = {ip: []}
        contents = json.dumps(everyone_dict,
                              sort_keys=True,
                              indent=4,
                              separators=(',', ':'))
        everyone_path.write_text(contents)
    result = {'result': [], 'g': 0, 'p': 0}

    def DrawCards():
        global Varg
        global Varp
        Varg = dictionary['gold']
        Varp = dictionary['purple']
        stars = 0
        color = int(float(random.randint(1, 100)))
        if Varg == 80 or color > 99:
            paid = Varg
            get = gc[random.randint(1, len(gc)) - 1]
            Varg = 0
            Varp = Varp + 1
            stars = 5
            result['result'].append({'name': get, 'star': stars})
            print(Fore.BLUE + ip + '花费了' + str(paid) + '抽，获得了5星: ' + get +
                  Fore.RESET)
            everyone_dict[ip].append({'paid': paid, 'name': get})
            everyone_contents = json.dumps(everyone_dict,
                                           sort_keys=True,
                                           indent=4,
                                           separators=(',', ':'))
            everyone_path.write_text(everyone_contents)
        elif Varp == 9 or color > 95:
            get = pc[random.randint(1, len(pc)) - 1]
            Varg = Varg + 1
            Varp = 0
            stars = 4
            result['result'].append({'name': get, 'star': stars})
        else:
            get = bc[random.randint(1, len(bc)) - 1]
            Varp = Varp + 1
            Varg = Varg + 1
            stars = 3
            result['result'].append({'name': get, 'star': stars})

    for i in range(int(times)):
        DrawCards()
        dictionary['gold'] = result["g"] = Varg
        dictionary['purple'] = result["p"] = Varp
        contents = json.dumps(dictionary,
                              sort_keys=True,
                              indent=4,
                              separators=(',', ':'))
        path.write_text(contents)
    return message('success', 201, result), 201


@limiter.exempt
@app.route('/talk', methods=['GET', 'POST'])
def talk():
    print(Fore.GREEN + request.form.get('ip') + ': ' +
          request.form.get('content') + Fore.RESET)
    return message('success', 200, 'Server gets the message.'), 200


@app.route('/list', methods=['GET', 'POST'])
def LuckyList():
    everyone_path = Path('./Data/everyone.json')
    everyone_dict = {}
    if everyone_path.exists():
        contents = everyone_path.read_text()
        everyone_dict = json.loads(contents)
    else:
        return message('error', 404, 'No one wished!'), 404
    return message('success', 200, everyone_dict), 200


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    ip = request.form.get('ip')
    path = Path('./Data/%s.json' % (ip))
    dictionary = {'ip': ip, 'gold': 0, 'purple': 0, 'paid': []}
    contents = json.dumps(dictionary,
                          sort_keys=True,
                          indent=4,
                          separators=(',', ':'))
    path.write_text(contents)
    return message('success', 200, 'Reset successfully!'), 200


@app.route('/quit', methods=['GET', 'POST'])
def quit():
    print(Fore.YELLOW + request.form.get('ip') + '断开了连接' + Fore.RESET)
    return message('success', 200, 'Quit successfully!'), 200


if __name__ == '__main__':
    app.run(debug=True, host=local_ip, port=5000)
