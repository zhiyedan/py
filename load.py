import MySQLdb
import time

start = time.time()
count = 10000

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

for line in file:
    item = line.split('\t')
    if (not item[1].strip() or item[5] == 'NULL' or item[6] == 'NULL'):
    # if (not item[1].strip() or item[1] == 'NULL' or not item[2].strip() or item[2] == 'NULL'):
        continue
    add_quotes(item,[0,1,2,3,10,11])
    item_str = ",".join(item)
    validData.append(item_str)

totalLen = len(validData)

sub_sql = ''

while len(validData) > 0 :
    for j in range(1,count):
        if len(validData)<=0:
            break
        sub_sql = (sub_sql + '(' +validData.pop()).strip('\r\n')+'),'
    sub_sql =  sub_sql.strip(',')
#    sql = "insert into mbk_ride17917 (user_id,reg_date,first_order_date,max_order_duration,order_cnt,sum_dist_km,sum_dura_hr,freq_district,max_order_date,max_order_cnt,rushhour_order_cnt,sum_redpacket,first_order_city,sum_order_day) values " + sub_sql
    sql =  "insert into users (name,age,birthday,grade) values " + sub_sql
    print 'sql is :' + sql
    cursor.execute(sql)
    conn.commit()
    print 'left '+str(len(validData))+' data, percent :' + str(len(validData)/totalLen) + '%'


cursor.close()
conn.close()
end = time.time() - start
print end

