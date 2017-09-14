#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import MySQLdb
import time

def getArgs():
    parse = argparse.ArgumentParser(prog = "load.py", usage="%(prog)s [options]")
    parse.add_argument('--host',type=str,help='host')
    parse.add_argument('-u',type=str,help='user')
    parse.add_argument('-p',type=str,help='passwd')
    parse.add_argument('--file',type=str,help='file path')

    args = parse.parse_args()
    return vars(args)


def main():
    args = getArgs()
    host = args['host']
    user = args['u']
    passwd = args['p']
    file_path = args['file']

    if(not host or not user or not file_path):
        print '输入参数有误'
        return

    start = time.time()
    count = 10000
    insert_field = 'user_id,reg_date,first_order_date,first_order_city,max_order_duration,order_cnt,sum_dist_km,sum_dura_hr,sum_order_day,sum_redpacket,freq_district,max_order_date,max_order_cnt,rushhour_order_cnt'
    # file_path = '/home/zhiyedan/Desktop/test3'

    config = {
        'host': host,
        'port': 3306,
        'user': user,
        'passwd': passwd,
        'db': 'mbk_activity',
        'charset': 'utf8'
    }
    conn = MySQLdb.connect(**config)
    conn.autocommit(1)
    cursor = conn.cursor()
    file = open(file_path,'r')

    def add_quotes(item,index):
        for i in index:
            item[i] = "\'" + item[i] + "\'"
        return

    round = 0
    num = 0
    sub_sql = ''

    for line in file:
        round += 1
        item = line.split('\t')
        # if (not item[1].strip() or item[5] == 'NULL' or item[6] == 'NULL'):
        if (not item[1].strip() or item[1] == 'NULL' or not item[2].strip() or item[2] == 'NULL' or item[5] == 'NULL' or item[6] == 'NULL'):
            continue
        add_quotes(item,[0,1,2,3,10,11])
        # add_quotes(item,[0,2])
        item_str = ",".join(item)

        sub_sql = sub_sql + '(' + item_str.strip('\r\n') + '),'
        # print 'sub sql is %s' % sub_sql
        num += 1
        if (num == count):
            sub_sql = sub_sql.strip(',')
            sql = "insert into mbk_ride17917 ("+ insert_field +") values " + sub_sql
            # print 'sql is :' + sql
            cursor.execute(sql)
            conn.commit()
            sub_sql = ''
            num = 0
            print " %d万 lines, time %d 秒 " % ((round/10000),(time.time()-start))

    if sub_sql:
        sub_sql = sub_sql.strip(',')
        sql = "insert into mbk_ride17917 (" + insert_field + ") values " + sub_sql
        # print 'sql is :' + sql
        cursor.execute(sql)
        conn.commit()

    cursor.close()
    conn.close()
    end = time.time() - start
    print 'total time is :%d 秒' % end

if __name__ == '__main__':
    main()
