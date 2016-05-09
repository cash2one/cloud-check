#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from scloud.shortcuts import *
from scloud.handlers import Handler

@url(r'/captcha', name="captcha")
class CaptchaHandler(Handler):
    def get(self):
        import os
        from imagecaptcha import Captcha
        font = os.path.join(scloud.base_path, 'static', 'fonts', 'arialbi.ttf')
        captcha = Captcha(FONT=font,
                          FONT_SIZE=30,
                          WIDTH=121,
                          HEIGHT=45,
                          PADDING=35,
                          BG_RGBA=(210, 214, 222),
                          FL_RGBA=(0, 0, 0),
                          CHAR="ABCDEFGHJKLMNPQRSTUVWXY345789")
        text, buf = captcha.gen()
        value = buf.getvalue()
        self.session["captcha"] = text.lower()
        self.save_session()
        self.set_header('Content-Type', 'image/jpeg; charset=utf-8')
        self.write(value)
