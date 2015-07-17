﻿# -*- coding: utf-8 -*-

from module.plugins.internal.MultiHoster import MultiHoster, create_getInfo


class FreeWayMe(MultiHoster):
    __name__    = "FreeWayMe"
    __type__    = "hoster"
    __version__ = "0.19"

    __pattern__ = r'https?://(?:www\.)?free-way\.(bz|me)/.+'
    __config__  = [("use_premium" , "bool", "Use premium account if available"    , True),
                   ("revertfailed", "bool", "Revert to standard download if fails", True)]

    __description__ = """FreeWayMe multi-hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("Nicolas Giese", "james@free-way.me")]


    def setup(self):
        self.resume_download = False
        self.multi_dl        = self.premium
        self.chunk_limit     = 1


    def handle_premium(self, pyfile):
        user, data = self.account.select_account()

        for _i in xrange(5):
            #: try it five times
            header = self.load("http://www.free-way.bz/load.php",  #@TODO: Revert to `https` in 0.4.10
                               get={'multiget': 7,
                                    'url'     : pyfile.url,
                                    'user'    : user,
                                    'pw'      : self.account.get_account_data(user)['password'],
                                    'json'    : ""},
                               just_header=True)

            if 'location' in header:
                headers = self.load(header['location'], just_header=True)
                if headers['code'] == 500:
                    #: error on 2nd stage
                    self.log_error(_("Error [stage2]"))
                else:
                    #: seems to work..
                    self.download(header['location'])
                    break
            else:
                #: error page first stage
                self.log_error(_("Error [stage1]"))

            #@TODO: handle errors


getInfo = create_getInfo(FreeWayMe)
