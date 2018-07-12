#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,io
from collections import defaultdict
import html_process as hp
import formatting as fmt
import regex
import check
import urllib


def washington_post(data_base,data_print,key,date):

    hp.login("kkk0001@sharklasers.com", "qazxdr12")

    kkey = fmt.file_name(key,'_')

    kkkey = fmt.file_name(key,'+')

    print("----- "+"washington_post."+kkey+" -----")
    print("Start loading Urls...")


    #case for exact keyword search
    url1='https://sitesearchapp.washingtonpost.com/sitesearch-api/v2/search.json?count=20&datefilter=displaydatetime:%5B*+TO+NOW%2FDAY%2B1DAY%5D&facets.fields=%7B!ex%3Dinclude%7Dcontenttype,%7B!ex%3Dinclude%7Dname&filter=%7B!tag%3Dinclude%7Dcontenttype:("Article"+OR+(contenttype:"Blog"+AND+name:("Opinions")))&highlight.fields=headline,body&highlight.on=true&highlight.snippets=1&query="'
    url2='"&sort=&startat='
    url3='&callback=angular.callbacks._0'
    baseurl = url1+kkkey+url2+'0'+url3

    try:
        page = hp.getHtml(baseurl)
    except urllib.error.URLError:
        pass

    article_number = regex.get_data('"total"\S(\S+?),"documents',page)[0]
    if article_number == 0:

        url1='https://sitesearchapp.washingtonpost.com/sitesearch-api/v2/search.json?count=20&datefilter=displaydatetime:%5B*+TO+NOW%2FDAY%2B1DAY%5D&facets.fields=%7B!ex%3Dinclude%7Dcontenttype,%7B!ex%3Dinclude%7Dname&filter=%7B!tag%3Dinclude%7Dcontenttype:("Article"+OR+(contenttype:"Blog"+AND+name:("Opinions")))&highlight.fields=headline,body&highlight.on=true&highlight.snippets=1&query='
        url2='&sort=&startat='
        url3='&callback=angular.callbacks._0'
        baseurl = url1+kkkey+url2+'0'+url3  

        try:
            page = hp.getHtml(baseurl)
        except urllib.error.URLError:
            print("Washington Post website is not correct, please check the code!")
            return -1

        article_number = regex.get_data('"total"\S(\S+?),"documents',page)[0]

        if article_number == 0:
            print("No Washington Post article was found by this key word")
            return -1

    #get all urls
    count = 0
    index = 0
    urls = []
    page_total = int(article_number) / 20 + 1
    while(count < page_total):

        currenturl = url1+key+url2+str(index)+url3
        try:
            page = hp.getHtml(currenturl)
        except urllib.error.URLError:
            continue

        url = regex.get_data('"contenturl"\S"(https:\/\/www.washingtonpost.com\/opinions/\S+?)"\S"',page)

        if date != 0:
            a_num = check.check_last_update(url,date)
            if a_num != -1:
                urls += url[:-(len(url)-a_num )]
                break

        urls += url

        index += 20
        count += 1
    

    print(str(len(urls))+" Urls loaded...")

    print("There are "+str(len(data_base)+len(data_print))+" loaded file...",)

    
    print("Now starting updating...",)
    count = 0
    #count2 = 0

    for url in urls:

        if url in data_base and kkey in data_base[url]:
            #if check.update_key(data_base, url, kkey):
            #    count2 += 1
            continue

        try:
            html = hp.getHtml(url)
        except urllib.error.URLError:
            continue


        title = regex.get_data('"headline":"(.*?)",',html)
        #<meta content="Julian Zelizer, CNN Political Analyst" name="author">
        author = regex.get_data('this.props.author="(.*?)";',html)
        #<meta content="2018-02-17T00:19:47Z" name="pubdate">
        date = regex.get_data('"datePublished":"(\S+?)T',html)
        
        text2 = regex.get_data('<article.*?>(.*?)<\/p>\s<\/article>',html)

        if text2 != []:
            text = regex.get_data('<p.*?>(.*?)<\/p>',text2[0])
        else:   
            text = regex.get_data('<p.*?>(.*?)<\/p>',html)     

        if text == [] or title == []:
            continue    

        data_print[url] = defaultdict(str)
        # line 1
        data_print[url]['ID'] = fmt.formatted_id(len(data_base)+len(data_print)-1)
        data_print[url]['key'] = fmt.formatted_key(kkey)
        # line 2
        data_print[url]['title'] = fmt.formatted_title(title)
        # line 3
        data_print[url]['source'] = fmt.formatted_source("Washington Post")
        # line 4
        data_print[url]['url'] = fmt.formatted_url(url)
        # line 5
        data_print[url]['date'] = fmt.formatted_date(date)
        # line 6
        data_print[url]['author'] = fmt.formatted_author(author,';')
        # line 7
        data_print[url]['content1'] = fmt.formatted_content_with_symbol(text)
        # line 8
        data_print[url]['content2'] = fmt.formatted_content(text)

        count += 1



    print("Updated "+str(count)+" articles...")
    #if count2 > 0:
    #    print("Updated "+str(count2)+" keys...")
    print("There are "+str(len(data_base)+len(data_print))+" articles...")

if __name__ == "__main__":
    data_base = {}
    check.load_previous(data_base)
    washington_post(data_base,'tax%20reform')
    import output_file
    output_file.output(data_base)