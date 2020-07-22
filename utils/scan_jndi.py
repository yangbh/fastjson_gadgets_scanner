#!/usr/bin/env python
# -*- coding: UTF-8 -*-


"""
Created on 2019/8/7 

@author: tmy
"""
import os
import sys
# from javalang.parse import parse
import javalang
from javalang.tree import *

UTIL_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(UTIL_DIR)
sys.path.append(UTIL_DIR)
sys.path.append(BASE_DIR)

from settings import FernFlower_PATH, FASTJSON_BLACK_LIST, SOURCE_DIR, RESULT_FILE
import logging
from lib import *

# 检验是否在白名单内
def in_black(filename):
    """
    判断是否在黑名单中
    :param filename:
    :return:
    """
    new_filename = filename.replace("/", ".")
    for _black in FASTJSON_BLACK_LIST:
        if _black in new_filename:
            return True
    return False


def clean(file_list):
    cache = {}

    for _file in file_list:
        if in_black(_file):
            continue

        # 通过 dict 去重
        new_filename = _file.split("/")
        key = new_filename[:7]
        key = ''.join(key)
        cache[key] = _file
        # new_file.append(_file)
    return cache.values()


def get_class_declaration(root):
    """
    筛选出符合条件的类
    :param root:
    :return:
    """
    class_list = []
    black_interface = ("DataSource", "RowSet")
    for node in root.types:
        # 非类声明都不分析
        if isinstance(node, ClassDeclaration) is False:
            continue

        # 判断是否继承至classloader
        if node.extends is not None and node.extends.name == "ClassLoader":
            continue

        # 判断是否实现被封禁的接口
        interface_flag = False
        if node.implements is None:
            node.implements = []
        for implement in node.implements:
            if implement.name in black_interface:
                interface_flag = True
                break
        if interface_flag is True:
            continue

        # 判断是否存在无参的构造函数
        constructor_flag = False
        for constructor_declaration in node.constructors:
            if len(constructor_declaration.parameters) == 0:
                constructor_flag = True
                break
        if constructor_flag is False:
            continue

        class_list.append(node)
    return class_list


def ack(method_node):
    """
    1、是否调用的lookup 方法，
    2、lookup中参数必须是变量
    3、lookup中的参数必须来自函数入参，或者类属性
    :param method_node:
    :return:
    """
    target_variables = []
    for path, node in method_node:
        # 是否调用lookup 方法
        if isinstance(node, MethodInvocation) and node.member == "lookup":
            # 只能有一个参数。
            if len(node.arguments) != 1:
                continue

            # 参数类型必须是变量，且必须可控
            arg = node.arguments[0]
            if isinstance(arg, Cast):    # 变量 类型强转
                target_variables.append(arg.expression.member)
            if isinstance(arg, MemberReference):  # 变量引用
                target_variables.append(arg.member)
            if isinstance(arg, This):       # this.name， 类的属性也是可控的
                return True
    if len(target_variables) == 0:
        return False

    # 判断lookup的参数，是否来自于方法的入参，只有来自入参才认为可控
    for parameter in method_node.parameters:
        parameter_name = parameter.name
        if parameter_name in target_variables:
            return True
    return False


def scan_jndi_gadgate(filename):
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
        class_declaration_list = get_class_declaration(root_tree)
        for class_declaration in class_declaration_list:
            for method_declare in class_declaration.methods:
                if ack(method_declare) is True:
                    string = "{file} {method}".format(file=filename, method=method_declare.name)
                    write_file(RESULT_FILE, string)
                    logging.warning(string)
                    return string
    except:
        return False

