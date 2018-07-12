#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, io
import re
import regex



def output(data_print, data_base, previous_len):

    invalid_file = 0;
    count = 0;

    index = previous_len
    f1 = open("Articles.bank", 'a',encoding='utf-8')
    for i in data_print:
        f2 = open("article\Article_"+str(index+count), 'w',encoding='utf-8')
        
        for j in data_print[i]:

            data_print[i][j] = re.sub(r'\\u\d+', ' ', data_print[i][j])
            data_print[i][j] = re.sub(r'[ ]+', ' ', data_print[i][j])

        if len(data_print[i]['title']) < 6 or len(data_print[i]['content']) < 10:


            invalid_file += 1
            continue

        f2.writelines(str(int(data_print[i]['ID']) - invalid_file)+'\n')
        f2.writelines(data_print[i]['key'])
        f2.writelines(data_print[i]['title'])
        f2.writelines(data_print[i]['source'])
        f2.writelines(data_print[i]['url'])
        f2.writelines(data_print[i]['date'])
        f2.writelines(data_print[i]['author'])
        f2.writelines(data_print[i]['content'])
        f1.writelines(data_print[i]['content'])


        count += 1


    print('Updated ',str(count), ' files in database...')





 
    '''
    f = open("news.bank", 'a',encoding='utf-8')
    for i in data_print:
        index = 0
        for j in data_print[i]:
            if index < 9:
                output = re.sub(r'\\u\d+', ' ', data_print[i][j])
                output = re.sub(r'[ ]+', ' ', output)
                f.writelines(output)

            
            index += 1
        f.writelines('\n')


    index1 = len(data_base)

    for i in data_print:
        f = open("article\Article"+str(index1)+".bank", 'w',encoding='utf-8')
        index2 = 0
        for j in data_print[i]:
            if index2 == 7:
                break

            output = re.sub(r'\\u\d+', ' ', data_print[i][j])
            output = re.sub(r'[ ]+', ' ', output)
            f.writelines(output)
            index2 += 1
        index1 += 1

    index1 = 0
    f = open("onlyArticles"+".bank", 'a',encoding='utf-8')
    for i in data_print:
        index2 = 0
        for j in data_print[i]:
            if index2 == 7:
                output = re.sub(r'\\u\d+', ' ', data_print[i][j])
                output = re.sub(r'[ ]+', ' ', output)
                f.writelines(output)


            index2 += 1
        index1 += 1
    '''


