#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
#========================================================================
#   FileName: request_log_analyzer_mysqllog.py
#     Author: Crazyunix
#      Email: crazyunix@163.com
#   HomePage: http://www.yunvi.com
# LastChange: 2013-04-23 15:29:37
#========================================================================
'''
import MySQLdb as mdb
import sys
import os
import glob
import time

path = '/opt/mysql/sandboxes/rsandbox_5_1_47/master/data'
slowlog='msandbox-slow.log'
when = time.strftime('%Y-%m-%d',time.localtime())
req_log = 'slow'+when

def Splitlog():
    if not os.path.isdir(path):
        print (path,'is not a dir !')
        sys.exit(0)
    try:
        os.chdir(path)
    except:
        print ("Permission denied")
        sys.exit(0)
    if not os.path.isfile('msandbox-slow.log'):
        print (path,'is not "msandbox-slow.log"')
        sys.exit(0)

    src_size = float('%.2f' % float('.'.join(str(x)for x in (divmod(os.path.getsize(slowlog),1024*1024)))))
    if src_size > 500:
        os.system("mv msandbox-slow.log mysql-slow")
        try:
            con = mdb.connect(host="localhost",user='root',passwd='',charset='utf-8',port=3306,unix_socket='/tmp/mysql.sock')
        except:
            print ('Could not connect to MySQL server!')
            sys.exit(0)
        try:
            #cur = con.cursor()
            #cur.execute("flush logs")
            #cur.execute("create database yong")
            con.close()
        except Exception,e:
            print e
            os.system("mv msandbox-slow.log msandbox-slow")
            sys.exit(0)
        os.system("split -b 500M msandbox-slow slow`date +%F`")
    else:
        os.system("mv msandbox-slow.log slow`date +%F`")
        try:
            con = mdb.connect("localhost",'root','','',25562)
        except:
            print ('Could not connect to MySQL server!')
            sys.exit(0)
        try:
            #cur = con.cursor()
            #cur.execute("flush logs")
            cur = con.cursor()
            cur.execute("show databases")
            print "Databases all : %s" % cur.fetchall()
            con.close()
        except:
            print ('Could not flush!')
            if os.path.isfile(path+req_log):
                os.system("mv slow`date +%F` msandbox-slow.log")
            sys.exit(0)


def Request_log():
    os.chdir(path)
    files=[os.path.basename(x) for x in  glob.glob(req_log + '*')]
    print files
    date=time.strftime("%Y-%m-%d",(time.localtime()))
    req = "request-log-analyzer %s/%s  --output HTML --mail ming.li@ihaveu.net --mailhost mail.haveu.net --mailsubject 'rails log-analyzer' --after %s" % ( path,files[-1],date)
    print req
    if len(files) == 1:
        os.system(req)
    else:
        for i in range(len(files)):
            req1 = "request-log-analyzer %s/%s  --output HTML --mail ming.li@ihaveu.net --mailhost mail.ihaveu.net --mailsubject 'rails log-analyzer' --after %s" % (path,files[i],date)
            os.system(req1)


def Remove_log():
    if os.path.isfile(path+'msandbox-slow'):
        os.system('mv /opt/mysql/sandboxes/rsandbox_5_1_47/master/data/msandbox-slow.log /opt/backup/mysql-slow')
        os.system('mv /opt/mysql/sandboxes/rsandbox_5_1_47/master/data/slow`date +%F`* /opt/backup-slow')
    else:
        os.system('mv /opt/mysql/sandboxes/rsandbox_5_1_47/master/data/slow`date +%F`* /opt/backup-slow')

    
if __name__ == '__main__':
   Splitlog()
   Request_log()
   Remove_log()
