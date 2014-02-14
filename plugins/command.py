#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   cold
#   E-mail  :   wh_linux@126.com
#   Date    :   14/01/16 12:18:53
#   Desc    :   相应基本命令插件
#
import time

from datetime import datetime

from plugins import BasePlugin
from plugins import config


class CommandPlugin(BasePlugin):
    def uptime(self):
        up_time = datetime.fromtimestamp(self.webqq.start_time)\
                .strftime("%H:%M:%S")
        now = time.time()

        sub = int(now - self.webqq.start_time)
        num, unit, oth = None, None, ""
        if sub < 60:
            num, unit = sub, "sec"
        elif sub > 60 and sub < 3600:
            num, unit = sub / 60, "min"
        elif sub > 3600 and sub < 86400:
            num = sub / 3600
            unit = ""
            num = "{0}:{1}".format("%02d" % num,
                                   ((sub - (num * 3600)) / 60))
        elif sub > 86400:
            num, unit = sub / 84600, "days"
            h = (sub - (num * 86400)) / 3600
            m = (sub - ((num * 86400) + h * 3600)) / 60
            if h or m:
                oth = ", {0}:{1}".format(h, m)

        return "{0} up {1} {2} {3}, handled {4} message(s)"\
                .format(up_time, num, unit, oth, self.webqq.msg_num)

    def msgon(self):
        config.SmartRobot_Enabled=True
        return u"消息群开启!!"
    def msgoff(self):
        config.SmartRobot_Enabled=False
        return u"消息群关闭!!!"
    def is_match(self, from_uin, content, type):
        ABOUT_STR = u"\nAuthor    :   evilbinary小E\nE-mail    :   rootntsd@gmail.com\n"\
                u"HomePage  :   http://blog.csdn.net/EvilBinary_root\n"\
                u"Project@  :   https://github.com/evilbinary"
        HELP_DOC = u"\n====命令列表====\n"\
        u"help         显示此信息\n"\
        u"ping         确定机器人是否在线\n"\
        u"about        查看关于该机器人项目的信息\n"\
		u"执行代码     lang:[语言] code:[代码]\n"\
        u">>> [代码]   执行Python语句\n"\
        u"-w [城市]    查询城市今明两天天气\n"\
        u"-tr [单词]   中英文互译\n"\
        u"-pm25 [城市] 查询城市当天PM2.5情况等\n"\
		u"-sleep	   关群消息\n"\
        u"====命令列表===="
        ping_cmd = "ping"
        about_cmd = "about"
        help_cmd = "help"
        msgoff_cmd="-sleep"
        msgon_cmd="-wake"
        commands = [ping_cmd, about_cmd, help_cmd, "uptime",msgoff_cmd,msgon_cmd]
        command_resp = {ping_cmd:u"小的在", about_cmd:ABOUT_STR,
                        help_cmd:HELP_DOC,
                        "uptime":self.uptime,msgoff_cmd:self.msgoff,msgon_cmd:self.msgon}

        if content.encode("utf-8").strip().lower() in commands:
            body = command_resp[content.encode("utf-8").strip().lower()]
            if not isinstance(body, (str, unicode)):
                body = body()
            self.body = body
            return True

    def handle_message(self, callback):
        callback(self.body)
