#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   evilbinary
#   E-mail  :   rootntsd@gmail.com
#   Date    :   2014-2-13 23:28
#   Desc    :   ���ýӿ�ʵ������lang����
#
import re
import logging
from bs4 import BeautifulSoup
from plugins import BasePlugin


logger = logging.getLogger("plugin")

class LangPlugin(BasePlugin):
    url = "http://www.compileonline.com/execute_new.php"
    result_p = re.compile(r'<pre>(.*?)</pre>', flags=re.U | re.M | re.S)

    def is_match(self, from_uin, content, type):
        lang_pos = content.find('lang:')
        if lang_pos < 6 and lang_pos >= 0:
            
            code_pos = content.find('code:')
            inputs_pos = content.find('inputs:')
            args_pos = content.find('args:')
            stdinput_pos = content.find('stdinput:')
            if inputs_pos == -1:
                inputs_pos = len(content)
            
            self._lang = content[lang_pos:code_pos][len('lang:'):].strip()
            self._code = content[code_pos:inputs_pos][len('code:'):].strip()
            self._inputs = content[inputs_pos:args_pos][len('inputs:'):].strip()
            self._args = content[args_pos:stdinput_pos][len('args:'):].strip()
            self._stdinput = content[stdinput_pos:-1][len('stdinput:'):].strip()
            self._header = ''
            
            print 'lang_pos:', lang_pos, 'code_pos:', code_pos, 'inputs_pos:', inputs_pos, 'args_pos:', args_pos, 'stdinput_pos:', stdinput_pos
            print 'lang:', self._lang
            print 'code:', self._code
            print 'input:', self._inputs
            print 'args:', self._args
            print 'stdinput:', self._stdinput
            
            return True
        return False

    def handle_message(self, callback):
        self.url = "http://www.compileonline.com/execute_new.php"
        params = {"args":self._args, "code":self._code.encode("utf-8"),
                  "inputs":self._stdinput, "lang": self._lang, "stdinput":self._stdinput}
        if self._lang in ['c', 'c++', 'c++11', 'c++0x', 'csharp', 'asm', 'ada', 'befunge', 'c99', 'cobol', 'cpp', \
                          'd', 'sdcc', 'erlang', 'fortran', 'fsharp', 'haskell', 'icon', 'ilasm', 'intercal', \
                          'java', 'mozart', 'nimrod', 'objc', 'ocaml', 'pascal', '"pawn', 'qbasic', \
                          'rust', 'scala', 'simula', 'vb.net', 'verilog']:
            params['header'] = ''
            params['support'] = ''
            params['util'] = ''
            print params
            self.url = "http://www.compileonline.com/compile_new.php"
 
            
        def read(resp):
            body = resp.body
            if len(resp.body) > 400:
                body = resp.body[0:400]
            try:
                logger.info(u"Lisp request success, result: {0}".format(body))
            except Exception, e:
                logger.info(u'except:{0}', e)

            try:
                soup = BeautifulSoup(resp.body)
                pre = soup.find_all('pre')
                result = ''
                if len(pre) == 0:
                    result = soup.get_text()
                for p in pre:
                    result = result + p.get_text()
            except Exception, e:
                logger.info(u'except:{0}', e)
                result = resp.body
			# result = self.result_p.findall(resp.body)
            # if not result else result[0]
            
            callback(result)
        
        self.http.post(self.url, params, callback=read)

