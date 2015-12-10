###监控系统stage1阶段设计文档
本阶段是单机数据采集器及其CLI开发

------------------------------------

####设计目标
* 采集对象： 单服务器
* 支持操作系统：
	* Arch
	* Debian 6,7
	* Ubuntu 11.04+
	* Linux Mint16+
	* CentOS 5,6,7
	* openSUSE
* 采集数据：
	* 平均负载
	* cpu使用率
	* 内存使用量

-----------------------------------------

####设计需求
设计并实现一个监控数据采集`agent`：采集平均负载、CPU使用率、内存使用等。

* 功能需求：

        Usage: python agent.py [Options]

        Options:
		  -v, --version show program version number and exit
		  -h, --help show this help message and exit
		  -t, --ttl set agent period, default is 60s
		  -m MODULE, --module=MODULE use module MODULE 

        Modules:
		  load, cpu, memory

* 设计需求：
	* 平均负载 - `load`需要采集以下三个指标：  
指标        含义  
w1\_avg    1分钟平均负载  
w5\_avg    5分钟平均负载  
w15\_avg   15分钟平均负载  
	* cpu使用率 - `cpu`需要采集以下指标，单位为百分比：  
指标  含义  
user 用户态  
nice 低优先级用户态  
system 内核态  
idle 空闲  
iowait 等待IO  
irq 硬中断服务  
softirq 软中断服务  
steal 虚拟化相关  
guest 虚拟化相关  
guest_nice 虚拟化相关  
	* 内存使用量 - `memory`需要采集以下指标，单位为字节：  
指标  含义  
total 总内存  
used 已使用内存  
abs_used used - buffers - cached  
free 空闲内存  
buffers 磁盘缓冲  
cached 磁盘缓存  
active 活跃内存，不大可能被挪用  
inactive 不活跃内存，很可能被挪用  
swap_used 已使用swap  

----------------------------------------

####功能设计
* 客户端设计  
客户端cli采用python封装，执行文件是根目录下 code/agent.py，基本操作如下：
	* 查看帮助
	* 查看版本号
	* 配置采集周期
	* 查看资源利用情况
* 后台设计  
服务器端采用shell进行数据采集
	* 负载信息获取方式：读取`/proc/loadavg`文件，输出为json格式文件
	* 内存信息获取方式：读取`/proc/meminfo`文件，输出为json格式文件
	* cpu信息获取方式：读取`/proc/stat`文件，输出为json格式文件
 
