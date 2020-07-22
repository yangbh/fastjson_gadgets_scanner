#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from settings import *
from lib import get_file_list, decomplier, get_java_file
import logging
from pprint import pprint

logging.basicConfig(level=logging.DEBUG)

def test_unpack():
    '''
    :return:
    '''
    files = get_file_list(MAVEN_DIR)
    print('total: %s' % len(files))
    # pprint(files)


def test_decomplier():
    '''
    :return:
    '''
    jar_file = '/Users/mody/.m2/repository/com/google/code/gson/gson/2.2.4/gson-2.2.4.jar'
    source_dir = decomplier(jar_file)
    print(source_dir)


def test_get_java_file():
    path = '/tmp/maven/source/gson-2.2.4'
    files = get_java_file(path)
    print('total: %s' % len(files))
    # pprint(files)


if __name__ == '__main__':
    # test_unpack()
    # test_decomplier()
    test_get_java_file()

