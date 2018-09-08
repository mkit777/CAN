import pymysql


class RadarDBClinet:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3306
        self.user = 'root'
        self.password = '111111'
        self.con = None
        self.cur = None


    def connect(self):
        self.con  = pymysql.connect(host='127.0.0.1',user='root',password='111111',db='radar',port=3306)
        return self

    def get_cur(self):
        if self.cur is None:
            self.cur = self.con.cursor()
        return self.cur

    def get_can_data(self):
        cur = self.get_cur()
        cur.execute('select * from can_data')
        return cur.fetchall()

    def update(self, order,frame_id):
        cur = self.get_cur()
        cur.execute(f'update can_data set frame_id={frame_id} where `order`={order}')
        self.con.commit()

if __name__ == '__main__':
    client = RadarDBClinet()
    client.connect()
    datas = client.get_can_data()
    
    frame_id = 0
    last_id= 1
    for data in datas:
        cur_id =data[1]
        if cur_id <= last_id:
            frame_id+=1
        client.update(data[0], frame_id)
        last_id= cur_id 
        print(cur_id)