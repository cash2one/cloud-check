#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

import os
from datetime import datetime
from fabric.api import hosts, run, cd, sudo, env, lcd, put, local, get
import sys

env.gateway = 'smt_app@192.168.0.35'

env.passwords = {'smt_app@192.168.0.35': 'smt_app'}

reload(sys)
sys.setdefaultencoding('utf-8')

@hosts("localhost")
def deploy():
    local("fab update restart")


@hosts("smt_app@192.168.3.145")
def update():
    env.password = "smt_app"
    with cd("/usr/api-root/webapps/scloud"):
        run("git pull")


@hosts("smt_app@192.168.3.145")
def restart():
    env.password = "smt_app"
    #with cd("/usr/api-root/supervisor/"):
    run("supervisorctl restart scloud")


@hosts("smt_app@192.168.3.145")
def start():
    env.password = "smt_app"
    # with cd("/usr/api-root/supervisor/"):
    run("supervisorctl start scloud")


@hosts("smt_app@192.168.3.145")
def stop():
    env.password = "smt_app"
    # with cd("/usr/api-root/supervisor/"):
    run("supervisorctl stop scloud")

