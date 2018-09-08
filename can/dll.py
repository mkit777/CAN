from ctypes import *
from can.err import raise_error
from can.models import *
libc = CDLL(r'dlls\ECanVci64.dll')

@raise_error('设备打开失败')
def open_device(dev_type, dev_index, reserved=0):
    '''
    打开设备
    Parameters
    dev_type: 设备类型号
    dev_index: 设备索引号
    reserved: 参数无意义
    Returns
    1 操作成功， 0 操作失败
    '''
    libc.OpenDevice.argtypes = [c_int, c_int, c_int]
    libc.OpenDevice.restype = c_int
    return libc.OpenDevice(dev_type, dev_index, reserved)


@raise_error('设备关闭失败')
def close_device(dev_type, dev_index):
    '''
    关闭设备
    Parameters
    dev_type: 设备类型号
    dev_index: 设备索引号
    Returns
    1 操作成功， 0 操作失败
    '''
    libc.CloseDevice.argtypes = [c_int, c_int]
    libc.CloseDevice.restype = c_int
    return libc.CloseDevice(dev_type, dev_index)


@raise_error('初始化CAN通道失败')
def init_can(dev_type, dev_index, can_index, p_init_config):
    '''
    初始化指定CAN通道
    Parameters
    dev_type: 设备类型号
    dev_index: 设备索引号
    can_index: 第几路CAN 
    p_init_config: 初始化结构体指针
    Returns:
    1成功 0失败
    '''
    libc.InitCAN.argtypes = [c_int, c_int, c_int, POINTER(INIT_CONFIG)]
    libc.InitCAN.restype = c_int
    return libc.InitCAN(dev_type, dev_index, can_index, p_init_config)


@raise_error('获取设备信息失败')
def read_board_info(dev_type, dev_index, p_info):
    '''
    获取设备信息
    Parameters:
    dev_type: 设备类型号
    dev_index: 设备索引号
    p_info: BOARD_INFO结构体指针
    Returns:
    1成功 0失败
    '''
    libc.ReadBoardInfo.argtypes = [c_int, c_int, POINTER(BOARD_INFO)]
    libc.ReadBoardInfo.restype = c_int
    print(libc.ReadBoardInfo(dev_type, dev_index, p_info))
    return libc.ReadBoardInfo(dev_type, dev_index, p_info)

@raise_error('获取错误信息失败')
def read_err_info(dev_type, dev_index, can_index, p_err_info):
    '''
    获取最后一次错误信息
    Parameters:
    dev_type: 设备类型号
    dev_index: 设备索引号
    can_index: CAN通道号
    p_err_info: ERR_INFO结构体指针
    Returns:
    1成功 0失败
    '''
    libc.ReadErrInfo.argtypes = [c_int, c_int, c_int, POINTER(ERR_INFO)]
    libc.ReadErrInfo.restype = c_int
    return libc.ReadErrInfo(dev_type, dev_index, can_index, p_err_info)

@raise_error('读取设备状态失败')
def read_can_status(dev_type, dev_index, can_index, p_can_status):
    '''
    获取CAN状态
    Parameters:
    dev_type: 设备类型号
    dev_index: 设备索引号
    can_index: CAN通道号
    p_can_status: CAN_STATUS结构体指针
    Returns:
    1成功 0失败
    '''
    libc.ReadCANStatus.argtypes = [c_int, c_int, c_int, POINTER(CAN_STATUS)]
    libc.ReadCanStatus.restype = c_int
    return libc.ReadCANStatus(dev_type, dev_index, can_index, p_can_status)

@raise_error('获取设备参数失败')
def get_reference(dev_type, dev_index, can_index, ref_type, p_data):
    '''
    获取设备的相应参数
    Parameters:
    dev_type: 设备类型号
    dev_index: 设备索引号
    can_index: CAN通道号
    ref_type: 参数类型
    p_data: 有关数据缓冲区地址首指针
    Returns:
    1成功 0失败
    '''
    libc.GetReference.argtypes = [c_int, c_int, c_int, c_int, c_void_p]
    libc.GetReference.restype = c_int
    return libc.GetReference(dev_type, dev_index. can_index, ref_type, p_data)

@raise_error('设置设备参数失败')
def set_reference(dev_type, dev_index, can_index, ref_type, p_data):
    '''
    设置设备相应参数
    Parameters:
    dev_type: 设备类型号
    dev_index: 设备索引号
    can_index: CAN通道号
    ref_type: 参数类型
    p_data: 有关数据缓冲区地址首指针
    Returns:
    1成功 0失败
    '''
    libc.SetReference.argtypes = [c_int, c_int, c_int, c_int, c_void_p]
    libc.SetReference.restype = c_int
    return libc.SetReference(dev_type, dev_index, can_index, ref_type, p_data)


def get_receive_num(dev_type, dev_index, can_index):
    '''
    获取指定缓冲区中接收到但尚未被读取的帧数量
    Parameters:
    dev_type: 设备类型号
    dev_index: 设备索引号
    can_index: CAN通道号
    Returns:
    尚未被读取的帧数
    '''
    libc.GetReceiveNum.argtypes = [c_int, c_int, c_int]
    libc.GetReceiveNum.restype = c_int
    return libc.GetReceiveNum(dev_type, dev_index, can_index)

@raise_error('清楚缓冲区失败')
def clear_buffer(dev_type, dev_index, can_index):
    '''
    清空指定CAN通道的缓冲区
    Parameters:
    dev_type: 设备类型号
    dev_index: 设备索引号
    can_index: CAN通道号
    Returns:
    1成功 0失败
    '''
    libc.ClearBuffer.argtypes = [c_int, c_int, c_int]
    libc.ClearBuffer.restype = c_int
    return libc.ClearBuffer(dev_type, dev_index, can_index)

@raise_error('启动CAN通道失败')
def start_can(dev_type, dev_index, can_index):
    '''
    启动指定CAN通道
    Parameters:
    dev_type: 设备类型号
    dev_index: 设备索引号
    can_index: CAN通道号
    Returns:
    1成功 0失败
    '''
    libc.StartCAN.argtypes = [c_int, c_int, c_int]
    libc.StartCAN.restype = c_int
    return libc.StartCAN(dev_type, dev_index, can_index)

@raise_error('发送数据失败')
def transmit(dev_type, dev_index, can_index, p_send, len):
    '''
    返回实际发送成功的帧数量
    Parameters:
    dev_type: 设备类型号
    dev_index: 设备索引号
    can_index: CAN通道号
    p_send: 要发送的数据帧的首指针
    len: 发送的数据帧数组的长度
    Returns:
    实际发送的帧数
    '''
    libc.Transmit.argtypes = [dev_type, dev_index,
                              can_index, POINTER(CAN_OBJ), c_int]
    libc.Transmit.restype = c_int
    return libc.Transmit(dev_type, dev_index, can_index, p_send, len)

@raise_error('接收数据失败', 0xffffffff)
def receive(dev_type, dev_index, can_index, p_receive, len, wait_time):
    '''
    从指定缓冲区里读取数据
    Parameters:
    dev_type: 设备类型号
    dev_index: 设备索引号
    can_index: CAN通道号
    p_reveive: 数据帧数组首指针
    len: 数据帧数组长度
    wait_time: 等待超时时间
    Returns:
    实际读到的帧数， 0xffffffff读取失败
    '''
    libc.Receive.argtypes = [c_int, c_int,
                             c_int, POINTER(CAN_OBJ), c_int, c_int]
    libc.Receive.restype = c_int
    return libc.Receive(dev_type, dev_index, can_index, p_receive, len, wait_time)

@raise_error('复位CAN失败')
def reset_can(dev_type, dev_index, can_index):
    '''
    复位CAN
    Parameters:
    dev_type: 设备类型号
    dev_index: 设备索引号
    can_index: CAN通道号
    Return:
    1成功 0失败
    '''
    libc.ResetCAN.argtypes = [c_int, c_int, c_int]
    libc.ResetCAN.restype = c_int
    return libc.ResetCAN(dev_type, dev_index, can_index)