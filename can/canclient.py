 
from can.dll import open_device, init_can, start_can, receive
from can.models import CAN_OBJ, INIT_CONFIG
from ctypes import pointer

class CANClient:
    def __init__(self, dev_type, dev_index):
        '''
        创建CAN客户端
        Parameters:
        dev_type: 设备类型
        dev_index: 设备索引
        '''
        self.dev_type = dev_type
        self.dev_index = dev_index
        self.has_init_can = False
        open_device(dev_type, dev_index)


    def init_can(self, can_index):
        '''
        初始化指定CAN通道
        Parameters:
        can_index: 通道号
        '''
        self.can_index = can_index
        init_config = INIT_CONFIG(
            AccCode=0,
            AccMask=0xFFFFFFFF,
            Filter=0,
            Timing0=0,
            Timing1=0x1c,
            Mode=0
        )
        init_can(self.dev_type, self.dev_index, can_index, pointer(init_config))
    

    def start_can(self):
        '''
        开启CAN通道
        '''
        ret = start_can(self.dev_type, self.dev_index, self.can_index)
        if ret == 1:
            self.has_init_can=True
    
    def receive_valid_one(self):
        '''
        接收一条有效的数据
        '''
        obj = CAN_OBJ()
        while True:
            receive(self.dev_type, self.dev_index, self.can_index, pointer(obj), 1, 1000)
            if obj.is_valid():
                return obj

    def receive_one(self, wait_time=50):
        '''
        接收一条数据
        '''
        obj = CAN_OBJ()
        receive(self.dev_type, self.dev_index, self.can_index, pointer(obj), 1, wait_time)
        return obj

    def receive_batch(self, wait_time=50):
        '''
        接收一批数据
        '''
        obj_array = (CAN_OBJ*32)()
        receive(self.dev_type, self.dev_index, self.can_index, obj_array, 32, wait_time)
        return [obj for obj in obj_array]