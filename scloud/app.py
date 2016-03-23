# -*- coding: utf-8 -*-

import os
import yaml
import uuid
import base64
import logging
import scloud
from torweb.application import make_application

application = make_application(scloud)
reverse_url = application.reverse_url
