#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import javalang
from javalang.tree import *

UTIL_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(UTIL_DIR)
sys.path.append(UTIL_DIR)
sys.path.append(BASE_DIR)




def scan_readObject(filename):
    '''
    核心逻辑
    :param filename:
    :return:
    '''
    try:
        file_stream = open(filename, 'r')
        _contents = file_stream.read()
        file_stream.close()

        # 字符串判断快速过滤
        if "InitialContext(" not in _contents:
            return False

        root_tree = javalang.parse.parse(_contents)

    except:
        return False
