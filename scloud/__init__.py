# -*- coding: utf-8 -*-


from os.path import abspath, dirname, join
base_path = abspath(dirname(__file__))

# 添加系统路径
import sys
sys.path.insert(0, abspath(join(base_path, '..', 'lib')))
from pprint import pprint
