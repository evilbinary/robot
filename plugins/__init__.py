#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   cold
#   E-mail  :   wh_linux@126.com
#   Date    :   14/01/16 11:21:19
#   Desc    :   插件机制
#   Modify  :   动态加载插件。rootntsd@gmail.com
import os
import inspect
import logging
import config
import sys
import thread
import threading
import time
import signal

logger = logging.getLogger("plugin")


class BasePlugin(object):
    """ 插件基类, 所有插件继承此基类, 并实现 hanlde_message 实例方法
    :param webqq: webqq.WebQQClient 实例
    :param http: TornadoHTTPClient 实例
    :param nickname: QQ 机器人的昵称
    :param logger: 日志
    """
    def __init__(self, webqq, http, nickname, logger = None):
        self.webqq = webqq
        self.http = http
        self.logger = logger or logging.getLogger("plugin")
        self.nickname = nickname

    def is_match(self, from_uin, content, type):
        """ 判断内容是否匹配本插件, 如匹配则调用 handle_message 方法
        :param from_uin: 发送消息人的uin
        :param content: 消息内容
        :param type: 消息类型(g: 群, s: 临时, b: 好友)
        :rtype: bool
        """
        return False

    def handle_message(self, callback):
        """ 每个插件需实现此实例方法
        :param callback: 发送消息的函数
        """
        raise NotImplemented



class MyThread(threading.Thread):
        def __init__(self, loader):  
                threading.Thread.__init__(self)
                self.loader=loader
                self.is_run=True
        def run(self):
            try:
                while self.is_run:
                    try:
                        self.loader.auto_load_plugins()
                        time.sleep(6) 
                    except KeyboardInterrupt:
                        logger.info("Exiting...Thread")
                        self.is_run=False
           
            except Exception,e:
                print 'Error',e
                logger.error(u"Plugin auto load  was encoutered an  error {0}".format(e), exc_info = True)
         
class PluginLoader(object):
    plugins = {}
    plugins_time={}
    def __init__(self, webqq):
        self.current_path = os.path.abspath(os.path.dirname(__file__))
        self.webqq = webqq
        self.auto_load_plugins()
        self.auot_load_thread=MyThread(self)
        self.auot_load_thread.start()
#         for m in self.list_modules():
#             mobj = self.import_module(m)
#             if mobj is not None:
#                 self.load_class(mobj)
        logger.info("Load Plugins: {0!r}".format(self.plugins))

    def list_modules(self):
        items = os.listdir(self.current_path)
        modules = [item.split(".")[0] for item in items
                   if item.endswith(".py")]
        return modules

    def import_module(self, m):
        try:
            sys.path.append(config.PLUGINS_DIR)
            filename="plugins." + m
            if sys.modules.has_key(filename):
                mod = sys.modules[filename]
                reload(mod)
                return mod
            else:
                return __import__(filename, fromlist=["plugins"])
        except:
            logger.warn("Error was encountered on loading {0}, will ignore it"
                        .format(m), exc_info = True)
            return None
   
            return None
    def load_class(self, m):
        for key, val in m.__dict__.items():
            if inspect.isclass(val) and issubclass(val, BasePlugin) and \
               val != BasePlugin:
                self.plugins[key] = val(self.webqq, self.webqq.hub.http,
                                        self.webqq.hub.nickname, logger)
                logger.info("Load Plugins  {0!r}succes!".format(key))
                
    def auto_load_plugins(self):
        for m in self.list_modules():
            file_name= self.current_path+'/'+m+'.py'
            if self.plugins_time.has_key(m):
                #print 'key:',m
                a=self.plugins_time[m]
                b=os.stat(file_name)
                #print 'a:', a.st_atime,' b:',b.st_atime
                if a==b:
                    #print 'equ'
                    pass
                else:
                    print 'x',m,b
                    logger.info("Load Plugins1: {0!r}".format(m))
                    if os.path.isfile(self.current_path+'/'+m+'.pyc'):
                        #os.remove(self.current_path+'/'+m+'.pyc')
                        pass
                    self.plugins_time[m]=b
                    mobj = self.import_module(m)
                    #mobj=self.reload_module(m)
                    if mobj is not None:
                        self.load_class(mobj)
            else:
                logger.info("Load Plugins: {0!r}".format(m))
                print "Load Plugins:",m
                self.plugins_time[m]=os.stat(file_name)
                mobj = self.import_module(m)
                if mobj is not None:
                    self.load_class(mobj)
#         print 'items:',self.plugins_time.keys()
        #print 'have nokey:',map(self.plugins_time.has_key,self.plugins.keys())
        pass
    def dispatch(self, from_uin, content, type, callback):
        """ 调度插件处理消息
        """
        
        try:
            for key, val in self.plugins.items():
                if val.is_match(from_uin, content, type):
                    try:
                        val.handle_message(callback)
                        logger.info(u"Plugin {0} handled message {1}".format(key, content))
                    except:
                        logger.error(u"Plugin {0} was encoutered an error"
                                     .format(key), exc_info = True)
                    else:
                        pass #return True
            return False
        except Exception,e:
            logger.error(u"dispatch {0} was encoutered an error",e)

if __name__ == "__main__":
    print 'test'
    p=PluginLoader(None)
    print 'modules:',p.list_modules()
    print 'plugins:',p.plugins,p.plugins_time
    
    pass
