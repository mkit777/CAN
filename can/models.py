from ctypes import *
from datetime import datetime


class BOARD_INFO(Structure):  # ReadBoardInfo中被填充
    '''
    hw_Version: 硬件版本号
    fw_Version: 固件版本号
    dr_Version: 驱动程序版本号
    in_Version: 接口库版本号
    irq_Num: 中断号
    can_Num: CAN通道数
    str_Serial_Num: 序列号 
    str_hw_Type: 硬件类型号
    Reserved: 系统保留
    '''
    _fields_ = [
        ('hw_Version', c_ushort),  # 硬件版本号
        ('fw_Version', c_ushort),  # 固件版本号
        ('dr_Version', c_ushort),  # 驱动程序版本号
        ('in_Version', c_ushort),  # 接口库版本号
        ('irq_Num', c_ushort),  # 板卡所使用中断号
        ('can_Num', c_char),  # 表示有几路CAN通道
        ('str_Serial_Num', c_char*20),  # 此板卡的序列号
        ('str_hw_Type', c_char*40),  # 硬件类型
        ('Reserved', c_ushort*4)  # 系统保留
    ]

    def __str__(self):
        return f'<硬件版本号{self.hw_Version} 固件版本号{self.fw_Version} 驱动程序版本号{self.dr_Version} 接口库版本号{self.in_Version} 中断号{self.irq_Num} CAN通道数{ self.can_Num.decode() } 序列号{self.str_Serial_Num.decode()} 硬件类型号{self.str_hw_Type.decode()}>'

    def to_dict(self):
        return {'hw_Version': self.hw_Version, 'fw_Version': self.fw_Version, 'dr_Version': self.dr_Version, 'in_Version': self.in_Version, 'irq_Num': self.irq_Num, 'can_Num': self.can_Num, 'str_Serial_Num': list(self.str_Serial_Num), 'str_hw_Type': list(self.str_hw_Type)}


class CAN_OBJ(Structure):  # Transmit Receive
    '''
    ID: 报文ID
    TimeStamp: 接收时间标识
    TimeFlag: 是否使用时间标识
    SendType: 发送帧类型 0正常发送 1单次发送 2自发自收 3单次自发自收
    RemoteFlag: 是否为远程帧 0数据帧 1远程帧
    ExternFlag: 是否为扩展帧 0标准帧 1扩展帧
    DataLen: Data的长度
    Data: 报文数据
    Reserved: 系统保留
    '''
    _fields_ = [
        ('ID', c_ulong),  # 报文帧ID
        ('TimeStamp', c_ulong),  # 接受信息时间戳
        ('TimeFlag', c_ubyte),  # 是否使用时间标识
        ('SendType', c_ubyte),  # 发送帧类型 0正常 1单次 2自发自收 3 单次自发自收
        ('RemoteFlag', c_ubyte),  # 是否是远程帧 0数据帧 1远程帧
        ('ExternFlag', c_ubyte),  # 是否是扩展帧 0 标准真 1扩展帧
        ('DataLen', c_ubyte),  # 数据长度
        ('Data', c_ubyte * 8),  # 报文数据
        ('Reserved', c_char*3)  # 系统保留
    ]

    def __str__(self):
        return f'<ID{self.ID} 时间戳{self.TimeStamp}>'

    def is_valid(self):
        return any(list(self.Data))

    @property
    def DataHex(self):
        return ' '.join([hex(x) for x in self.Data])

    @property
    def DataParsed(self):
        return self._parse_data()

    def db_handler(self):
        return (self.ID, self.TimeStamp, datetime.now(), self.TimeFlag, self.SendType, self.RemoteFlag, self.ExternFlag, self.DataLen, self.DataHex, *self.DataParsed)

    def _parse_data(self):
        data = self.Data
        range = self.__parse_range(data) * 0.1
        angle = self.__parse_angle(data) * 0.1
        speed = self.__parse_speed(data) * 0.01
        rcs = self.__parse_rcs(data) * 0.005
        return range, angle, speed, rcs

    def __parse_range(self, data):
        range = (data[0] << 3)+(data[1] >> 5)
        return range

    def __parse_angle(self, data):
        angle_ori = ((data[1] << 5)+(data[2] >> 3)) & 0b111111111
        if data[1] >> 4 & 1 == 1:
            angle = -((angle_ori-1) ^ 0b111111111)
        else:
            angle = angle_ori & 0b111111111
        return angle

    def __parse_speed(self, data):
        speed_ori = ((data[4] << 6) + (data[5] >> 2)) & 0b1111111111111
        if data[4] >> 7 & 1 == 1:
            speed = -((speed_ori-1) ^ 0b1111111111111)
        else:
            speed = speed_ori
        return speed

    def __parse_rcs(self, data):
        rcs_ori = ((data[6] << 8)+(data[7])) & 0b111111111111111
        if data[6] >> 7 & 1 == 1:
            rcs = -((rcs_ori-1) ^ 0b111111111111111)
        else:
            rcs = rcs_ori
        return rcs


class CAN_STATUS(Structure):  # ReadCanStatus
    '''
    ErrInterrupt: 中断记录
    regMode: 模式寄存器
    regStatus: 状态寄存器
    regALCapture: 仲裁丢失寄存器
    regECCapture: 错误寄存器
    regEWLimit 错误警告限制寄存器
    regRECounter: 接收错误寄存器
    regTECounter: 发送错误寄存器
    Reserved: 系统保留 
    '''
    _fields_ = [
        ('ErrInterrupt', c_char),  # 中断记录，读操作会清除
        ('regMode', c_char),  # 模式寄存器
        ('regStatus', c_char),  # 状态寄存器
        ('regALCapture', c_char),  # 仲裁丢失寄存器
        ('regECCapture', c_char),  # 错误寄存器
        ('regEWLimit', c_char),  # 错误警告限制寄存器
        ('regRECounter', c_char),  # 接受错误寄存器
        ('regTECounter', c_char),  # 发送错误寄存器
        ('Reserved', c_int)  # 系统保留
    ]


class ERR_INFO(Structure):
    '''
    ErrCode: 错误码
    Passive_ErrData: 消极错误的错误标识数据
    ArLost_ErrData: 仲裁丢失错误的错误标识数据
    '''
    _fields_ = [
        ('ErrCode', c_uint),
        ('Passive_ErrData', c_ubyte*3),
        ('ArLost_ErrData', c_ubyte)
    ]

    def __str__(self):
        return f'<错误码{hex(self.ErrCode)} 消极错误表示{list(self.Passive_ErrData)} 仲裁错误标识{self.ArLost_ErrData}>'


class INIT_CONFIG(Structure):
    '''
    AccCode: 验收码
    AccMask: 屏蔽码
    Reserved: 保留
    Filter: 滤波使能
    Timing0: 波特率定时器0
    Timing1: 波特率定时器1
    Mode: 模式 0正常 1只听 2自发自收
    '''
    _fields_ = [
        ('AccCode', c_int),  # 验收码
        ('AccMask', c_int),  # 屏蔽码
        ('Reserved', c_int),  # 保留
        ('Filter', c_char),  # 滤波使能
        ('Timing0', c_char),  # 波特率定时器0
        ('Timing1', c_char),  # 波特率定时器1
        ('Mode', c_char)  # 模式 0正常 1只听 2自发自收
    ]


class FILTER_RECORD(Structure):
    '''
    ExtFrame: 过滤帧类型标志 1扩展帧 0标准帧
    Start: 滤波范围的起始帧ID
    End: 滤波范围的结束帧ID
    '''
    _fields_ = [
        ('ExtFrame', c_int),
        ('Start', c_int),
        ('End', c_int)
    ]
