#!/usr/bin/env python
# -*- coding: UTF-8 -*-


"""
Created on 2019/8/7

@author: tmy
"""
import os
import sys

UTIL_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(UTIL_DIR)
sys.path.append(UTIL_DIR)
sys.path.append(BASE_DIR)

from settings import FernFlower_PATH, FASTJSON_BLACK_LIST, SOURCE_DIR, RESULT_FILE
import logging


def get_file_list(path):
    """
    获取目录下所有文件
    :param path:
    :return:
    """
    path = os.path.abspath(path)
    _file_list = []

    if os.path.exists(path) is False:
        return _file_list

    file_list = os.listdir(path)
    for _file in file_list:
        file = os.path.join(path, _file)
        if os.path.isfile(file):
            if _file.endswith(".jar") and "javadoc" not in _file:
                _file_list.append(file)
        else:
            _file_list.extend(get_file_list(file))

    return _file_list


def decomplier(file):
    """
    反编译
    :param file:
    :return:
    """
    cmd = 'java -jar %s -dgs=true %s %s' % (FernFlower_PATH, file, SOURCE_DIR)
    logging.debug(cmd)
    os.system(cmd)

    jar_file_name = file.split('/')[-1]
    jar_file_path = SOURCE_DIR + jar_file_name

    target_dir = jar_file_name.split('.')[:-1]
    source_dir = '.'.join(target_dir)
    source_dir = SOURCE_DIR + source_dir
    unzip_cmd = 'unzip -n %s -d %s' % (jar_file_path, source_dir)
    # unzip_cmd = 'unzip ' + jar_file_path + " -d " + source_dir + " > /dev/null 2>&1"
    logging.debug(unzip_cmd)
    os.system(unzip_cmd)
    return source_dir


def get_java_file(source_path):
    if os.path.exists(source_path) is False:
        return []

    path = os.path.abspath(source_path)

    _file_list = []
    file_list = os.listdir(path)
    for _file in file_list:
        file = os.path.join(path, _file)
        if os.path.isfile(file):
            if _file.endswith(".java"):
                _file_list.append(file)
        else:
            _file_list.extend(get_java_file(file))
    return _file_list



def write_file(filename, string):
    file_stream = open(filename, "a")
    file_stream.write(string + '\n')
    file_stream.close()


def read_file(filename):
    try:
        file_stream = open(filename, 'r')
        _contents = file_stream.read()
        file_stream.close()
        scanner_list = _contents.strip().split('\n')
    except:
        return []
    return scanner_list
