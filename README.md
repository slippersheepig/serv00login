- action保号被github封掉了，于是仿一个docker版的放vps上，再用crontab之类的定时工具执行，执行结果推送到电报
  + 理论上支持运行docker容器的平台都可以使用本项目
  + 定时工具各有所爱，自行选择即可
- 附上docker-compose.yml样例
- ```bash
  services:
    login:
      image: sheepgreen/serv00login
      container_name: login
      environment:
        TELEGRAM_BOT_TOKEN: 1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ
        TELEGRAM_CHAT_ID: 9876543210
        PUSH: telegram
        SSH_INFO: '[{"hostname": "panelXXX.serv00.com", "username": "name", "password": "pass"}]'
  ```
