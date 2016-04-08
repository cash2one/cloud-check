# -*- coding: utf-8 -*-

import os
import yaml
import uuid
import base64
import logging
import scloud
from scloud.config import tornado_settings
from torweb.application import make_application
from tornado.web import RequestHandler

application = make_application(scloud)
reverse_url = application.reverse_url
def static_url(path):
    logger.info(path)
    return RequestHandler.make_static_url(tornado_settings, path)
