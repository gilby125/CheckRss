# -*- coding: utf-8 -*-

import os
import sys
import time
import feedparser as fp
import smtplib
import requests

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders


List_word = []
List_word.append("error")
List_word.append("mistake")
List_word.append("misprice")
List_word.append("icn")
List_word.append("seoul")
List_word.append("tokyo")
List_word.append("korea")
List_word.append("japan")
List_word.append("hongkong")
List_word.append("mileage run")
List_word.append("super")
List_word.append("asia")
List_word.append("ASIANA")
List_word.append("OZ")

SOURCE_FILE_NAME = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname("rss_source.ini"))) 
RESULT_FILE_NAME = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname("old_rss.log"))) 

def check_word(p_title):
    f_ok = 0
    for t_word in List_word:
        if p_title.find(t_word) >= 0:
            f_ok = 1
            break
    return f_ok

def read_source():
    l_source_list = []
            
    with open(SOURCE_FILE_NAME, 'r') as f_read:   
        for each_line in f_read:
            if each_line[0:1] == "#":
                continue
            l_source_list.append(each_line[:-1])
            
    return l_source_list

def is_old_rss(p_site, p_title, p_link):
    l_rtn = 0
    with open(RESULT_FILE_NAME, 'r') as f_read:   
        for each_line in f_read:           
            t_item = each_line.split('\t')
            #print p_link, t_item[3]
            if t_item[3].strip() == p_link:
                l_rtn = 1
                break
    #print l_rtn        
    return l_rtn


def write_log(p_log):
    l_tm = time.strftime("%y%m%d:%H%M%S",time.localtime())
    f = open(RESULT_FILE_NAME, 'a')
    f.write(l_tm + '\t' + p_log + '\n')
    f.flush()
    f.close()

def send_mail(p_log):
    '''
    l_from = 'koreawk@naver.com'
    l_to = 'wonkyu@gmail.com'

    msg = MIMEText(p_log,'html')
 
    msg['Subject'] = 'CHECK RSS'
    msg['From'] = l_from
    msg['To'] = l_to
 
    mailServer=smtplib.SMTP("smtp.naver.com",587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(l_from,'suukyunaverkwh1224')
    mailServer.sendmail(l_from, l_to, msg.as_string())
    mailServer.close()
    '''
    data = 'from=wonkyu@gmail.com&to=wonkyu@gmail.com&subject=CHECK_RSS&msg=' + p_log
    print data
    r =  requests.post("http://wk-emailer-1046.appspot.com/post", data=data)
    #write_log (str(r.status_code))
                
if __name__=='__main__':
    l_msg = ''
    SITES = read_source()
    for SITE in SITES:    
        FEEDS = fp.parse(SITE)
        #print "@ " + SITE[:-1]
        for post in FEEDS.entries:
            if check_word(post.title.lower()) :
                if is_old_rss(SITE, post.title, post.link) == 1 : 
                    continue
                t_str = SITE + "\t" + post.title + "\t" + post.link
                t_str = t_str.encode("cp949", "ignore")
                print t_str
                write_log (t_str)
                l_msg += t_str + '\n'
    
    if l_msg <> '':
        send_mail(l_msg)