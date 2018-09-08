from can.canclient import CANClient
from can.db import DBClinet
from datetime import datetime
from functools import partial
import sys
import os

def main():
    print('开始运行')
    db = DBClinet('127.0.0.1', 'root',
                  '111111', 'radar', 3306)
    sql = 'insert into can_data (id,timestamp,receive_time,time_flag,send_type,remote_flag,extern_flag,data_len,data_hex,`range`,angle,speed,rcs)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'

    can_data_storage = db.get_auto_storage(10, sql, has_handler=True)
    print('数据库连接正常')

    can = CANClient(3, 0)
    print('设备开启正常')

    can.init_can(0)
    print('CAN初始化正常')

    can.start_can()
    print('CAN启动正常')

    total = 0
    while True:
        obj = can.receive_valid_one()
        can_data_storage.store(obj)
        total += 1
        show(obj, total)

def show(obj, total):
    data =obj.DataParsed
    print(f'总计{total}\torder{total}\tid{obj.ID}\ttimestamp{obj.TimeStamp}\trange{round(data[0],2) }\tangle{round(data[1],2)}\tspeed{round(data[2],2)}\trcs{round(data[3],2)}')

if __name__ == '__main__':
    main()