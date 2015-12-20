####拷贝代码
git clone github.com/lokikiller/trainning.git

####设置数据库信息
docker pull mongo
docker run -p 27017:27017 -v /tmp/mongo/data:/data/db -d mongo

####启动监测脚本
进到代码目录data里 然后python filter.py

####启动监测脚本rest服务
进到代码目录data里 然后python server.py

####启动展示层服务
python router.py


####现有问题：
1.	缺少主机注册页面及监测启停按钮
2.	服务容器化，代码相关调整，涉及到访问地址等环境变量配置
3.	容器化之后，展示层的访问地址部分代码需要相关调整
4.	Dockerfile及文档编写