# -*- coding: utf-8 -*-

import json
import requests
import re
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

'''
def get_hotlist_text(url):

    response = requests.get(url)
    code = response.text
    
    with open('output.html','w') as file:
        file.write(code)

    print("saved")
    
    return feed_text


def print_json_keys(json):

#    for key, value in json.items():
#        print(f"Key: {key}, Value: {value}")
    for key, value in json.items():
        print(f"Key: {key}")
    
'''

def get_list_text(url):
    #long_string = 'some long string with "hotList" and "hotListHeadZone" in between'
    response = requests.get(url)
    long_string = response.text
    start_index = long_string.find('"hotList":') + len('"hotList":')
    end_index = long_string.find(',"hotListHeadZone"')

    desired_string = long_string[start_index:end_index]

 #   print(desired_string)

    return desired_string

def get_saved_list():

    # 检查文件是否存在
    if not os.path.exists("saved.json"):
    # 如果文件不存在，则创建并写入默认内容
        with open("saved.json", "w") as file:
            default_data = [{"title": "No Record", "link": "https://flask.yakumo2.uk", "itemID": "0", "cardId": "Q", "new": False}]
            json.dump(default_data, file)

    with open("saved.json", 'r', encoding='utf-8') as file:
        file_content = file.read()

    print("read from saved json")

    return file_content

def get_live_list():

    list_text = get_list_text("https://www.zhihu.com/billboard")
    return parse_feed(list_text)

def save_list(code):
    with open('saved.json','w') as file:
        file.write(code)

    print("saved")
    return None

def parse_feed(json_string):
    
   # data = "[" + content + "]"
    parsed_data = json.loads(json_string)

    feed_list = []
    
    for item in parsed_data:
        title = item['target']['titleArea']['text']
        link = item['target']['link']['url']

        itemID = item['id']
        parts = itemID.split("_")
        if len(parts) > 0:
            itemID = parts[0]
            print(itemID)
        else:
            print("can't get ID")

        cardId = item['cardId']

        block = {
            'title': title,
            'link': link,
            'itemID': itemID,
            'cardId': cardId,
            'new': True,
            'isRead': False
        }

        feed_list.append(block)

    feed_json = json.dumps(feed_list, ensure_ascii=False)

    return feed_json

def print_feed_json(feed_json):

    feed = json.loads(feed_json)

    for item in feed:
        print(item['cardId'])
        print(item['itemID'])
        print(item['title'])
        print(item['link'])


#live_list = get_live_list()
#print(live_list)

#save_list(live_list)


def pull_feed():
    live_list = get_live_list()

#    save_list(live_list)

    return live_list


def updateList():

    live_list = json.loads(pull_feed())
    saved_list = json.loads(get_saved_list())

    for saved_entry in saved_list:
        cardId = saved_entry.get('cardId')
        for live_entry in live_list:
            if live_entry['cardId'] == cardId:
                live_entry['new'] = False  # 将 live_list 中的条目标记为已读
                live_entry['isRead'] = saved_entry['isRead']  # 将 live_list 中的 isRead 设为与 saved_list 中相同的值
                break

    print("updated")
    
    return json.dumps(live_list)

@app.route('/update')  # 只接受 POST 请求
def update_data():
    # 在这里执行更新操作
    # 例如，调用你的更新函数或者重新获取数据等
    # 更新成功时返回 HTTP 状态码 200，表示成功
    # 如果有任何错误，返回适当的错误码
    # 例如，返回 HTTP 状态码 500 表示服务器内部错误
    try:
        # 执行更新操作
        # 这里可以根据你的具体需求来实现更新逻辑
        # 例如，调用获取数据的函数、更新数据库等
        
        # 假设更新成功
        temp = updateList()
        save_list(temp)
        print("网页更新")
        return '更新成功', 200
    except Exception as e:
        print("更新失败:", e)
        return '更新失败', 500


@app.route('/markAsRead', methods=['GET'])  # 只接受 POST 请求
def markAsRead():
    cardId = request.args.get('cardId')
    print(cardId)
    # 这里添加标记为已读的逻辑

    try:
        with open('saved.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，则创建一个空的数据
        data = [{"title": "No Record", "link": "https://flask.yakumo2.uk", "itemID": "0", "cardId": "Q", "new": False}]

    # 设置要查找的 cardId
    target_card_id = cardId

    # 遍历数据，查找包含指定 cardId 的块，并将其 isRead 设置为 True
    for entry in data:
        if entry["cardId"] == target_card_id:
            entry["isRead"] = True

    # 将更新后的数据保存回 saved.json
    with open('saved.json', 'w') as file:
        json.dump(data, file, indent=4)


    response_data = {'message': 'Marked as read: {}'.format(cardId)}
    return jsonify(response_data)

@app.route('/')
def index():
    
 #   saved_list = get_saved_list()
    #print(saved_list)

 #   live_list = get_live_list()
#   save_list(live_list)
#   print(live_list)
#    current_list = updateList()
#    current_list = pull_feed()

    current_list = get_saved_list()

    feed_json = json.loads(current_list)

    return render_template('index.html', feed=feed_json)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=15000)
