import MySQLdb

# db设置
DB_HOST = '192.168.0.105'
DB_PORT = 3306
DB_USERNAME = 'root'
DB_PASSWORD = '123456'
DB_NAME = 'rtz'


class DbCorporation:
    def __init__(self):
        self.conn = MySQLdb.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USERNAME,
            passwd=DB_PASSWORD,
            db=DB_NAME,
            charset='utf8mb4',
        )
        self.cur = self.conn.cursor()

    def get_data_from_db(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def get_num_from_db(self, table_name):
        self.cur.execute('select count(1) as number from %s' % table_name)
        return self.cur.fetchone()

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    db = DbCorporation()
    for i in range(0, 10):
        rows = db.get_data_from_db('select * from fs_rtz order by id limit %s,%s' % (i * 10, 10))
        for j in range(len(rows)):
            print(rows[j])

    num = db.get_num_from_db('fs_rtz')

    db.close()
