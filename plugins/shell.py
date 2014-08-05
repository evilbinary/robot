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
import logging
import inspect
import os

logger = logging.getLogger("plugin")

def callit(obj, mname, args=[]):
    mth = eval('obj.%s'%(mname))
    if callable(mth):
        return apply(mth, args)
    else:
        return mth

class ShellPlugin(BasePlugin):
    pre_fix="!@#"
    def is_match(self, from_uin, content, type):
        self.send_content=''
        if content.startswith(self.pre_fix):
            try:
                content=content.strip(self.pre_fix);
#                 if content.startswith('list'):
#                     content=content.lstrip('list')
#                     if content=='':
#                         self.send_content=dir(self)
#                     else:
#                         self.send_content=inspect.getargspec(getattr(self,content.lstrip(' ')))
#                     pass
#                 elif content=='show':
#                     self.send_content='show'
#                     pass
#                 else:
    #                 if hasattr(self,content):
                funname=content.split(" ")[0]
                content=content.strip(funname)
                #fun=getattr(self,funname)
                self.send_content=self.send_content+' '+funname
                print 'content:',content
                args=[]
                if content!='':
                    args=list(content.split(','))
#                     if args[0]=='':
#                         args=[]
                print args,len(args)
                self.send_content=callit(self,funname,args)
#                 else:
#                     #self.send_content=dir('self.'+content)
#                     pass
                pass
            except Exception,e:
                self.send_content=e
                logger.error(u"Plugin  was encoutered an  error {0}".format(e), exc_info = True)
            return True
        return False

    def handle_message(self, callback):
        callback(self.send_content)
        return True
    def test(self):
        print 'test'
        return 'hello'
    def ls(self,args=[]):
        return os.popen('ls '+''.join(args)).read()

if __name__=="__main__":
    s=ShellPlugin(None,None,None,None)
    s.is_match(1,'!@#test','s')
    s.is_match(1,'!@#pre_fix','s')
    print s.send_content
