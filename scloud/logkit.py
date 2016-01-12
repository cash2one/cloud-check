#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from torweb.logkit import iColoredConsoleFormatter

class ColoredConsoleFormatter(iColoredConsoleFormatter):
    # colored_format = '[%(levelname)1.1s][%(asctime)s] %(message)s'
    colored_format = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'

