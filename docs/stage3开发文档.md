###stage3开发文档

----------------------

####数据提交接口 ./code/data/kafkaProducer.py
收集机器的监控数据，通过kafka的生产者对象
写入kafka队列。主要功能继承了上一阶段的filter.py

-----------------------

####解耦数据提交接口和数据处理模块的中间件

* 中间件选择kafka
在每台机器上启动kafkaProducer.py，采集数据，写入
kafka,由于kafkaConsumer.py目前采用简单消费者模型
，如果启动多个消费者，存在重复消费问题，因此只需
要在一台机器上启动storage服务。

-----------------------

####启停脚本

* 服务管理方式：
	System-V style init script

* 脚本:./script/run.sh

-----------------------
####web升级

* JQuery进行网页设计
