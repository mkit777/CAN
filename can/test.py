def parse_data(data):
    range = parse_range(data) 
    angle = parse_angle(data)
    speed = parse_speed(data) 
    rcs = parse_rcs(data)
    return range, angle, speed, rcs

def parse_range( data):
    range = ((data[0] << 3)+(data[1] >> 5))&0b1111111111
    print('range', bin(range))
    return range

def parse_angle( data):
    angle_ori = ((data[1] << 5)+(data[2] >> 3)) & 0b111111111
    print('angle', bin(angle_ori))
    if data[1] >> 4 & 1 == 1:
        angle = -((angle_ori-1) ^ 0b111111111)
    else:
        angle = angle_ori & 0b111111111
    return angle

def parse_speed( data):
    speed_ori = ((data[4] << 6) + (data[5] >> 2)) & 0b1111111111111
    print('speed', bin(speed_ori))
    if data[4] >> 7 & 1 == 1:
        speed = -((speed_ori-1) ^ 0b1111111111111)
    else:
        speed = speed_ori
    return speed

def parse_rcs( data):
    rcs_ori = ((data[6] << 8)+(data[7])) & 0b111111111111111
    print('rcs', bin(rcs_ori))
    if data[6] >> 7 & 1 == 1:
        rcs = -((rcs_ori-1) ^ 0b111111111111111)
    else:
        rcs = rcs_ori
    return rcs

if __name__ == '__main__':
    data=[0x0c, 0xbf, 0xa0, 0x00, 0xff, 0xcc,0x00, 0x63]
    ret = parse_data(data)
    print(ret)


