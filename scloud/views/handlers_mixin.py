# -*- coding: utf-8 -*-

import re
# import urlparse
from scloud.config import logger


class HandlersMixin(object):

    @property    
    def bread_list(self):
        return []

    def filter_pjax(self, referer_url):
        find_list = re.compile(".*([&]_pjax=[\S]+).*").findall(referer_url)
        for key in find_list:
            referer_url = referer_url.replace(key, "")
        return referer_url

    def handler_return_url(self):
        request = self.request
        logger.info("\t" + "*" * 30 + "\n")
        logger.info("\t [request]: %s" % dir(request))
        logger.info("\t [referer]: %s" % request.headers.get("Referer", ""))
        full_url = self.filter_pjax(self.request.full_url())
        logger.info("\t [full_url]: %s" % full_url)
        referer_url = self.filter_pjax(request.headers.get("Referer", ""))

        if full_url == referer_url:
            pass
        else:
            if referer_url:
                self.session["from_url"] = referer_url
                self.save_session()
        logger.info("\t [from_url]: %s" % self.session.get("from_url"))
        logger.info("\t" + "*" * 30 + "\n")
