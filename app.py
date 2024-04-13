from flask import Flask, request, Response, jsonify, render_template, send_from_directory
import requests
import json
import os

openai_api_base_url = os.environ['OPENAI_API_BASE_URL']
openai_api_key = os.environ['OPENAI_API_KEY']
openai_api_key = os.environ['PROMPT']
prompt = os.environ['PROMPT']

app = Flask(__name__)


driver_messages = []

def find_driver_message(driver) -> list:
    for message in driver_messages:
        if message['driver'] == driver:
            # 判断内容是否大于8000字符
            if len(message['messages']) < 8000:
                return message['messages']
    message = {
        'driver': driver,
        'messages': [
            {
                'role': 'system',
                'content': prompt
            }
        ]
    }
    driver_messages.append(message)
    return message['messages']
            
def save_driver_message(driver, res_message):
    for message in driver_messages:
        if message['driver'] == driver:
            message['messages'].append(res_message)
            print('res message: ', res_message)
            return

def send_text_to_gpt(messages):
    while True:
        url = f'{openai_api_base_url}/chat/completions'
        payload = json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "stream": False
        })
        headers = {
            'Authorization': f'Bearer {openai_api_key}',
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json'
        }

        print('req: ', json.dumps(messages, ensure_ascii=False))
        res = requests.post(url=url, data=payload, headers=headers, verify=False)
        print(res.text)
        if 'error' in res.text:
            print("正在重试中...")
            continue
        return res.json()['choices'][0]['message']



@app.route('/v1/chat', methods=['POST'])
def chat():
    args = request.get_json()
    print('接收到用户输入：', args)
    driver = args['driver']
    text = args['text']
    messages = find_driver_message(driver)
    messages.append({
        'role': 'user',
        'content': text
    })
    res_message_item = send_text_to_gpt(messages)
    save_driver_message(driver, res_message_item)
    content = res_message_item['content']
    
    # 创建一个Response对象，设置内容为字符串"我很好"，编码为UTF-8
    response_content = content
    # response_content = "哈哈哈"
    response = Response(response_content, status=200, content_type='text/plain; charset=utf-8')

    return response

    

if __name__ == '__main__':
    # 判断环境变量是否都设置
    if not all([openai_api_base_url, openai_api_key, prompt]):
        print('环境变量未设置')
        exit(1)
    app.run(host='0.0.0.0', port=8081, debug=True)