# -*- coding: utf-8 -*-

import re
import time

from module.plugins.internal.Account import Account


class NowVideoSx(Account):
    __name__    = "NowVideoSx"
    __type__    = "account"
    __version__ = "0.05"

    __description__ = """NowVideo.at account plugin"""
    __license__     = "GPLv3"
    __authors__     = [("Walter Purcaro", "vuolter@gmail.com")]


    VALID_UNTIL_PATTERN = r'>Your premium membership expires on: (.+?)<'


    def load_account_info(self, user, req):
        validuntil  = None
        trafficleft = -1
        premium     = None

        html = self.load("http://www.nowvideo.sx/premium.php", req=req)

        m = re.search(self.VALID_UNTIL_PATTERN, html)
        if m:
            expiredate = m.group(1).strip()
            self.log_debug("Expire date: " + expiredate)

            try:
                validuntil = time.mktime(time.strptime(expiredate, "%Y-%b-%d"))

            except Exception, e:
                self.log_error(e)

            else:
                if validuntil > time.mktime(time.gmtime()):
                    premium = True
                else:
                    premium = False
                    validuntil = -1

        return {"validuntil": validuntil, "trafficleft": trafficleft, "premium": premium}


    def login(self, user, data, req):
        html = self.load("http://www.nowvideo.sx/login.php",
                         post={'user': user,
                               'pass': data['password']},
                         req=req)

        if re.search(r'>Log In<', html):
            self.wrong_password()
