from functools import wraps


class CANException(Exception):
    '''
    CAN操作异常
    '''
    def __init__(self, message):
        self.message = message


def raise_error(err_message=None,err_code=0):
    if err_message is None:
        err_message = '操作失败'
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            if ret == err_code:
                raise CANException(err_message)
            else:
                return ret
        return wrapper
    return decorate
