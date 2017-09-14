import MySQLdb
import time

import sys


def main(argv):

start = time.time()
count = 2

file_path = '/home/zhiyedan/Desktop/test2'

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': 'sj',
    'db': 'test',
    'charset': 'utf8'
}
conn = MySQLdb.connect(**config)
conn.autocommit(1)
cursor = conn.cursor()

file = open(file_path,'r')

validData = []

def add_quotes(item,index):
    for i in index:
        item[i] = "\'" + item[i] + "\'"
    return

num = 0

sub_sql = ''

for line in file:
    item = line.split('\t')
    # if (not item[1].strip() or item[5] == 'NULL' or item[6] == 'NULL'):
    if (not item[1].strip() or item[1] == 'NULL' or not item[2].strip() or item[2] == 'NULL'):
        continue
    # add_quotes(item,[0,1,2,3,10,11])
    add_quotes(item,[0,2])
    item_str = ",".join(item)

    sub_sql = sub_sql + '(' + item_str.strip('\r\n') + '),'
    print 'sub sql is %s' % sub_sql
    num += 1
    if (num == count):
        sub_sql = sub_sql.strip(',')
        sql = "insert into users (name,age,birthday,grade) values " + sub_sql
        print 'sql is :' + sql
        cursor.execute(sql)
        conn.commit()
        sub_sql = ''
        num = 0

if sub_sql:
    sub_sql = sub_sql.strip(',')
    sql = "insert into users (name,age,birthday,grade) values " + sub_sql
    print 'sql is :' + sql
    cursor.execute(sql)
    conn.commit()

cursor.close()
conn.close()
end = time.time() - start
print 'total time is :%d' % end

if __name__ == '__main__':
    main(sys.argv)
