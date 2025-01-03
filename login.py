import os
import paramiko
import requests
import json
from datetime import datetime, timezone, timedelta

def execute_ssh_command(hostname, username, password, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=22, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode().strip()
        ssh.close()
        return result
    except Exception as e:
        print(f"连接 {hostname} 时出错: {str(e)}")
        return None

def ssh_multiple_connections(hosts_info, command):
    results = []
    for host_info in hosts_info:
        result = execute_ssh_command(
            hostname=host_info['hostname'],
            username=host_info['username'],
            password=host_info['password'],
            command=command
        )
        if result:
            results.append((result, host_info['hostname']))
    return results

def telegram_push(message):
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
    payload = {
        'chat_id': os.getenv('TELEGRAM_CHAT_ID'),
        'text': message,
        'parse_mode': 'HTML'
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"发送消息到Telegram失败: {response.text}")

def main():
    ssh_info_str = os.getenv('SSH_INFO', '[]')
    hosts_info = json.loads(ssh_info_str)
    command = 'whoami'

    results = ssh_multiple_connections(hosts_info, command)
    content = "SSH服务器登录信息：\n"
    for user, hostname in results:
        content += f"用户名：{user}，服务器：{hostname}\n"

    beijing_timezone = timezone(timedelta(hours=8))
    time = datetime.now(beijing_timezone).strftime('%Y-%m-%d %H:%M:%S')
    content += f"本次登录用户共： {len(results)} 个\n登录时间：{time}"

    if os.getenv('PUSH') == "telegram":
        telegram_push(content)
    else:
        print("推送失败，推送参数设置错误")

if __name__ == '__main__':
    main()
