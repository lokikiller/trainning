###监控系统stage1阶段需求文档
考虑对于单台服务器的系统监控，需要设计和完成一个采集数据的agent，定时采集数据存储到数据库中，并提供web接口和页面来查看采集的监控数据。

单台服务器agent程序开发，采集指标包括三种类型，平均负载、CPU使用率、内存使用量

####开发需求:
1. 理解涉及的监控指标含义
2. 明确这些指标用哪些命令查看，如何操作
3. 调研采集方法并实现
4. 采集周期可配置
5. 输出简单设计文档

####采集指标:

w1\_avg    1分钟平均负载
w5\_avg    5分钟平均负载
w15\_avg   15分钟平均负载

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

total 总内存
used 已使用内存
abs_used used - buffers - cached
free 空闲内存
buffers 磁盘缓冲
cached 磁盘缓存
active 活跃内存，不大可能被挪用
inactive 不活跃内存，很可能被挪用
swap_used 已使用swap
