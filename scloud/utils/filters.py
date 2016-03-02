#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from datetime import datetime
import urllib2


class Filters(object):
    @classmethod
    def init(cls, env):
        method_prefix = 'filter_'
        flts = Filters()
        methods = dir(flts)
        for m in methods:
            if not m.startswith(method_prefix): continue
            fname = m[len(method_prefix):]
            env.filters[fname] = flts.__getattribute__(m)

    def filter_urlquote(self, value):
        return urllib2.quote(value)

    def filter_urlunquote(self, value):
        return urllib2.unquote(value)

    def filter_getGoodTime(self, time_str):
        if isinstance(time_str, datetime):
            t = time_str
        else:
            t = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        retstr = ''
        if not t: return u'N/A'
        if datetime.now() < t: return u'N/A'
        delta = datetime.now() - t
        if delta.days >= 30: retstr = t.strftime('%Y-%m-%d')
        elif delta.days >= 1: retstr = u'%d天前' % (delta.days)
        elif delta.seconds < 60: retstr = u'刚刚'
        elif delta.seconds < 3600: retstr = u'%d分钟前' % (delta.seconds / 60)
        elif delta.seconds < 86400: retstr = u'%d小时前' % (delta.seconds / 3600)
        else: retstr = u'%d小时前' % (delta.seconds / 3600)
        return retstr

    def filter_format_datetime(self, time_str):
        if time_str:
            if type(time_str) == "str":
                t = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            else:
                t = time_str
            retstr = ''
            if not t: return u'N/A'
            if t >= datetime.strptime("9999-12-31 23:59:59", "%Y-%m-%d %H:%M:%S"):
                return ''
            return t.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return ''
