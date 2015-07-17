# -*- coding: utf-8 -*-

import xml.dom.minidom as dom

from module.plugins.internal.Account import Account


class RealdebridCom(Account):
    __name__    = "RealdebridCom"
    __type__    = "account"
    __version__ = "0.48"

    __description__ = """Real-Debrid.com account plugin"""
    __license__     = "GPLv3"
    __authors__     = [("Devirex Hazzard", "naibaf_11@yahoo.de")]


    def load_account_info(self, user, req):
        if self.pin_code:
            return

        html = self.load("https://real-debrid.com/api/account.php", req=req)
        xml  = dom.parseString(html)

        validuntil = float(xml.getElementsByTagName("expiration")[0].childNodes[0].nodeValue)

        return {'validuntil' : validuntil,
                'trafficleft': -1        ,
                'premium'    : True      }


    def login(self, user, data, req):
        self.pin_code = False

        html = self.load("https://real-debrid.com/ajax/login.php",
                         get={"user": user,
                              "pass": data['password']},
                         req=req)

        if "Your login informations are incorrect" in html:
            self.wrong_password()

        elif "PIN Code required" in html:
            self.log_warning(_("PIN code required. Please login to https://real-debrid.com using the PIN or disable the double authentication in your control panel on https://real-debrid.com"))
            self.pin_code = True
