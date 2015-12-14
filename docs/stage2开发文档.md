###stage2开发文档

----------------------

####数据采集器
python封装数据采集器，dataCollection.py

* cpu 采集器： getCpuData()
* memory采集器： getMemory()
* load采集器： getLoad()


-----------------------

####数据持久化

* 数据库选择mongoDB
* 数据集
	* cpu\mem\load3个collection
	* 字段设计：timestamp hostname+ip data
* 持久化算法设计：
	* 总体思想为取每个阶段最大值，采用队列实现
	* 以30s为单位进行数据采集
	* 分别创建1min、5min、30min、1day 4个队列
	* 1min队列长度为2，5min队列长度为5，30分钟队列长度为6，1day队列长度为24
	* 每个队列满长度时，将队列中最大值推送至下一个队列，并清空该队列。如：1min队列长度为2时，选择队列中的最大值，推送给5min队列，并清空1min队列

-----------------------

####逻辑控制

* 选型：
	* flask
* 路由：
	* / 展示界面 index.html

-----------------------

####数据展示

* 选型：
	* angular js
	* highchart js
	* smoothie-chart js
	* bootstrap css

* 路由：
	* /system-status 展示层集合
		* cpu-chart cpu历史数据展示 highchart
		* mem-chart memory历史数据展示 highchart
		* load-chart load历史数据展示 highchart
		* cpu-avg-load-chart load动态数据展示 smoothie
		* memory-info memory信息展示
		* cpu-info cpu信息展示
	* /loading
	* 详见原稿设计与stage2 demo  