#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   rootntsd
#   E-mail  :   rootntsd@gmail.com
#   Date    :   14/01/26 0:35:00
#   Desc    :   '''
#
#from __init__ import BasePlugin
from plugins import BasePlugin

import config
from bs4 import BeautifulSoup
import random

from tornadohttpclient import TornadoHTTPClient
try:
    import sys 
    reload(sys) 
    sys.setdefaultencoding('utf8')
except Exception,e:
                print 'except',e

class Searcher(object):
    
    def __init__(self, http = None):
        self.http = http or TornadoHTTPClient()
        #self.http.debug=True
        self.result=[]
        self.statment=[]
        self.helpkeyword=['?',u'怎么',u'什么',u'鸭子','ee',u'好了','YY','yy',u'神马',u'啊',u'？',u'是么',u'依依',u'EE',u'BSD鸭子',u'能不能',u'多少',u'么']
        pass
    def parse(self,content):
        self.statment.append(content.split('?'))
        return len(self.statment)
    def search(self,content):
        count=self.parse(content)
        for c in self.statment:
            t=''.join(c)
            print 'statment:',t
            self.result.append(self.baidu_know_search(t))
            print 'after:',self.result
        print 'count:',count
        return count
    def get_result(self):
        print 'get_result:',type(self.result),len(self.result)
        ret=''
        if len(self.result)>0:
            number=random.randint(0, len(self.result)-1)
            print 'number:',number,'len:',len(self.result)-1
            rets=self.result[number]
            if len(rets)>0:
                ret=''.join(rets[0])
                print 'ret:',ret,type(ret)
                return ret
        return ret
    def baidu_search(self,content):
        try:
            print 'baidu_search' 
            result=[]
            def getdata(response):
                #print(response.headers)
                #print(self.http.cookie)
                #print 'body:',response.body
                #print 'error',response.error
                body=response.body
                
                if len(body)<=10:
                    return
                #soup = BeautifulSoup(body,'html5lib') #do not enable ,'html5lib'
                soup = BeautifulSoup(body)
                
                #print(soup.prettify())
                #for link in soup.find_all('a'):
                #    print(link.get('href'))
                #print(soup.get_text())
                '''find normal'''
                #tds=soup.find_all('td',class_='c-default') #why no work in linux i dont know why ,who can answer?
                tds=soup.find_all('div',attrs={'class':'result c-container'})
                print type(tds)
                print len(tds)
                for i in range(len(tds)):
                    h3=tds[i].find('h3')
                    div=tds[i].find_all('div',attrs={'class':'c-abstract'})
                    if h3!=None:
                        print i,'h3:',h3.get_text()
                        for d in div:
                            print i,'txt:',d.get_text()
                            result.append(d.get_text())
                             
                    else:
                        print i,'no:',tds[i].get_text()
                '''find baike'''
                tds=soup.find_all('div',attrs={'class':'result-op c-container xpath-log'})
                print type(tds)
                print len(tds)
                for i in range(len(tds)):
                    h3=tds[i].find('h3')
                    div=tds[i].find_all('div')
                    if h3!=None:
                        print i,'h3:',h3.get_text()
                        for d in div:
                            print i,'txt:',d.get_text()
                    else:
                        print i,'no:',tds[i].get_text()

#                 '''find new'''
#                 tds=soup.find_all('div',id='content_left')
#                 print '======:',len(tds),tds[0].get_text()

    #             for td in tds:
    #                 #print td
    #                 h3=td.find('h3')
    #                 div=td.find_all('div',class_='c-abstract')
    #                 if h3!=None:
    #                     print 'h3:',h3.get_text()
    #                 for d in div:
    #                     print 'txt:',d.get_text()
                #for l in container:
                #    print l
                #content_left=container.<div id="content_left">
    #             tabs=soup.find_all('table',_class='result')
    #             for d in tabs:
    #                 print 'h',d.get('h3')
                #self.http.stop()
                ran=0
                data='.....'
                if len(result)>0:
                    ran=random.randint(0,len(result)-1)
                    data=result[ran]
                print 'self.http.stop',len(result),' rand:',ran
                print 'send:',data
                if self.send_msg!=None:
                    s=data
                    s=s.lstrip(' ')
                    s=s.lstrip('最佳答案:')
                    s=s.lstrip('问题描述:')
                    s=s.lstrip('最佳答案:')
                    s=s.lstrip('问题描述:')
                    s=s.rstrip('最佳答案:')
                    s=s.rstrip('问题描述:')
                    s=s.lstrip(' ')
                    #s=s.split(' ')[0]
                   
                    self.send_msg(s)
            try:
                url="http://www.baidu.com/s?wd="+content
                self.http.get(url, callback = getdata)
                #self.http.start()
            except KeyboardInterrupt:
                print("exiting...")
            except Exception,e:
                print 'except',e
            return result
        except Exception,e:
            print 'except:',e
    
    def baidu_know_search(self,content):
        try:
            print 'baidu_know_search' 
            result=[]
            def getdata(response):
                #print(response.headers)
                #print(self.http.cookie)
                #print 'body:',response.body
                #print 'error',response.error
                body=response.body
                
                if len(body)<=10:
                    return
                #soup = BeautifulSoup(body,'html5lib') #do not enable ,'html5lib'
                soup = BeautifulSoup(body)
                
                #print(soup.prettify())
                #for link in soup.find_all('a'):
                #    print(link.get('href'))
                #print(soup.get_text())
                '''find normal'''
                #tds=soup.find_all('td',class_='c-default') #why no work in linux i dont know why ,who can answer?
                dls=soup.find_all('div',attrs={'class':'list'})
                print type(dls)
                print len(dls)
                for i in range(len(dls)):
                    #answer=dls[i].find('h3')
                    
                    answer=dls[i].find_all('dd',attrs={'class':'dd answer'})
                    print 'type answer:',type(answer)
                    print 'answer:',answer
                    if answer!=None:
                        for d in range(len(answer)):
                            print 'answer d:',d , answer[d].get_text()
                            result.append(answer[d].get_text())
                             
                    else:
                        print i,'no:',dls[i].get_text()
 
                

#                 '''find new'''
#                 tds=soup.find_all('div',id='content_left')
#                 print '======:',len(tds),tds[0].get_text()

    #             for td in tds:
    #                 #print td
    #                 h3=td.find('h3')
    #                 div=td.find_all('div',class_='c-abstract')
    #                 if h3!=None:
    #                     print 'h3:',h3.get_text()
    #                 for d in div:
    #                     print 'txt:',d.get_text()
                #for l in container:
                #    print l
                #content_left=container.<div id="content_left">
    #             tabs=soup.find_all('table',_class='result')
    #             for d in tabs:
    #                 print 'h',d.get('h3')
                #self.http.stop()
                ran=0
                data='.....'
                if len(result)>0:
                    ran=random.randint(0,len(result)-1)
                    data=result[ran]
                print 'self.http.stop',len(result),' rand:',ran
                print 'send:',data
                if self.send_msg!=None:
                    s=data
                    s=s.lstrip('答：')
                    #s=s.split(' ')[0]
                   
                    self.send_msg(s)
            try:
                url="http://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=utf8&word="+content
                self.http.get(url, callback = getdata)
                #self.http.start()
            except KeyboardInterrupt:
                print("exiting...")
            except Exception,e:
                print 'except',e
            return result
        except Exception,e:
            print 'except:',e
            
    def find(self,content):
        print 'find '+content
        if self.findKey(content):
            #print '找到'
            return True
        else:
            return False
            #print '没找到'
        return False
    def findKey(self,content):
        for key in self.helpkeyword:
            #print key
            if content.find(key)>-1:
                return True;
        return False

class SmartRobotPlugin(BasePlugin):
    def get_result(self):
        return self.searcher.get_result()

    def handle_message(self, callback):
#         data=self.get_result()
#         #data='aa'
#         print 'send data:',data
#         callback(data)
#         print 'callback end'
        self.callback=callback
        self.searcher.send_msg=self.callback
        pass
    def is_match(self, from_uin, content,type):
        #print 'from_uin:',from_uin," content:",content," type:",type
        if not getattr(config, "SmartRobot_Enabled", False):
            return False
        else:
            self.searcher = Searcher()

#        print 'is match'
        if type == "g" or type=="s" or type=="b":
            print 'search'
            if self.searcher.find(content):
                result=self.searcher.search(content)
                if result>=0 :
                    print 'result count:',result
                    
                    return True
        else:
            self.content = content
            return True
        return False
        pass
if __name__ == "__main__":
    c=TornadoHTTPClient()
    #c.start()
    robot=SmartRobotPlugin(None,None,None,None)
    #while True:
  
    if robot.is_match(111, 'ss?', 'g')==True:
        data=robot.get_result()
        print "data:",data,type(data)
    else:
        print 'no found'
    c=TornadoHTTPClient()
    s=Searcher(c)
    c.start()
    #s.baidu_search('ss')
    c.stop()
#     
    pass
    
