###监控系统stage1阶段用户文档
用户通过CLI使用单机采集程序，程序入口为code/agent.py

主要操作：
1. 查看版本
    `python agent.py -v`
2. 获取帮助
    `python agent.py -h`
3. 配置采集周期
    `python agent.py -t [time]`
    该参数为可选参数，单位为秒
4. 采集模块选择
    `python agent.py -m [MODULE]`
    MODULE包括load,cpu,memory
