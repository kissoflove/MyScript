#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import os.path

import csv


#遍历指定路径下的csv文档
SOURCEPATH = "/Users/Wade/Documents/convert_csv_file"#不能用~代替
OKPATH= '%s/convertOK ' % SOURCEPATH

for file in os.listdir(SOURCEPATH):
    # print(file)
    if 'csv' in file :
        print(file)
        #操作文件
        #1.截取文件名称中的SN
        sn = file.split('_')[2]
        print(sn)
        
        #2.获取文件中的第3列（9，10，11，12行）
        if os.path.isfile(file):
            fd = open(file,"r")
            data = fd.readlines()      
            #直接将文件中按行读到list里
            print(data)
            dcr = data[8].split(',')[2]
            # print(dcr)
            rs  = data[9].split(',')[2]
            ls  = data[10].split(',')[2]
            q   = data[11].split(',')[2]
             
            newline = "%s,%s,%s,%s,%s" % (sn,dcr,rs,ls,q) +'\n'

            print(newline)
            #3.写入到新文件中
            if not os.path.exists(OKPATH):
                os.makedirs(OKPATH)
                print OKPATH + ' 创建成功'
            #4.
            tmp = '%s' % OKPATH +'/converted.csv'
            fm = open(tmp,'a+')#追加
            fm.write(newline)

            #fd.close()
        