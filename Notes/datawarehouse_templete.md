## pySQL模板

``` python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ******************************************************************************
# Name:     #.py
# Description:
# Input:
# Target Database： 
# Target Table:     #
# Source Template:     #
# Created By:     eliseowang
# Modified:     2021-05-31
# Version:     v1.0
# ******************************************************************************

 # python内部变量
time = __import__('time')
datetime = __import__('datetime')
string = __import__('string')

# 设定执行参数，整体只需要配置一次，避免出错
database_name = ""  # 数据库名
target_table_name = ""  # 目标表名

def createPartition(tdw, iDay): # 建表函数，一般按照日期分区
    sql = "USE {}".format(database_name) # 选定数据库
    tdw.execute(sql)

    sql = """
    CREATE TABLE IF NOT EXISTS {}(

    )
    PARTITION BY LIST()(
       PARTITION 
    )
    """.format(target_table_name)
    try: # 尝试创建表，并写日志
        tdw.execute(sql)
    except:
        tdw.WriteLog(("excute sql errror ,sql:{} ").format(sql))
    # 新增分区，新增当前日期iDay分区
    sql = "ALTER TABLE {} PARTATION (p_{})".format(target_table_name,  iDay)
    tdw.WriteLog(("execute sql: {}".format(sql))) # 创建日志，记录创建\修改的分区信息

def insertData(tdw, iDay): # 填充数据函数
    sql = 'use {}'.format(database_name) # 选定数据库
    tdw.execute(sql) 
 
    sql = """ 
    INSERT INTO
    TABLE {}()
    """.format(target_table_name) #填充数据，按照建表字段填充

def TDW_PL(tdw, argv=[]):
    inDate = argv[0] # 获取当前系统时间
    iDay = (datetime.datetime.strptime(inDate, "%Y%m%d") +
            datetime.timedelta(days=6)).strftime("%Y%m%d") # 获取YYYYMMDD格式日期
    print(iDay) # 输出日期，校验
    createPartition(tdw, iDay) # 分区，如果有表就创建分区
    tdw.WriteLog("create partition over") # 写日志，创建分区结束
    insertData(tdw, iDay) # 填充数据
    tdw.WriteLog("insert date over") # 写日志，填充数据结束

```

## 4. 有用的python语法

### 字符串拼接

``` python
# 用占位符的方法，将iDay作为参数拼接到字符串中
'abcd %(iDay)s efg'% {'iDay':iDay}
# 将iDay作为参数拼接到字符串中，format函数和占位符可以同时使用
# 如果多个位置用到了同一个参数，用占位符比较好
"""
  INSERT INTO TABLE {}
  SELECT '%(iDay)s' as date 
""".format(tablename)% {'iDay':iDay}
```

### `striptime()` 和 `striftime()`

* `striptime(string[, format])`根据指定的格式把一个时间字符串解析为时间元组。

``` python
import time
time.strptime("30 Nov 00", "%d %b %y")   
# 输出：time.struct_time(tm_year=2000, tm_mon=11, tm_mday=30, tm_hour=0, tm_min=0,
#                 tm_sec=0, tm_wday=3, tm_yday=335, tm_isdst=-1)

```