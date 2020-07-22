#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# author: yangbh

import os
import sys
import logging
from utils.RunCmd import RunCmd
from utils.lib import *
from utils.scan_jndi import scan_jndi_gadgate, clean
from settings import *
from pprint import pprint, pformat

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    # filename='logs/scanner.log'
                )

def checkJar(jar_file):
    '''检查一个文件
    '''
    try:
        logging.info(jar_file)
        source_dir = decomplier(jar_file)
        logging.info('source_dir: %s' % source_dir)
        class_files = get_java_file(source_dir)
        logging.info('total class: %s' % len(class_files))
        if not jar_file:
            return False
        for class_file in class_files:
            try:
                logging.info('scanning %s %s ' % (jar_file, class_file))
                if class_file:
                    scan_jndi_gadgate(class_file)
            except Exception as e:
                logging.error(e, exc_info=True)

    except Exception as e:
        logging.error(e, exc_info=True)

    return True


def main(maven_dir=MAVEN_DIR,jar_file=None):
    '''
    :return:
    '''
    if jar_file:
        checkJar(jar_file)
    elif maven_dir:
        print('maven_dir: %s' % maven_dir)
        jar_files = get_file_list(maven_dir)
        print('total: %s' % len(jar_files))
        logging.warning('total jars: %s' % len(jar_files))

        for jar_file in jar_files:
            checkJar(jar_file)

    scanner_list = read_file(RESULT_FILE)
    results = clean(scanner_list)
    logging.info('--------Gadgets-------')
    logging.warning(pformat(results))


def usage():
    print('usage: python %s [maven_dir]' % __file__)
    exit(1)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        usage()

    elif len(sys.argv) == 2:
        if os.path.isdir(sys.argv[1]):
            main(maven_dir=sys.argv[1])
        elif os.path.isfile(sys.argv[1]):
            main(jar_file=sys.argv[1])

    elif len(sys.argv) == 1:
        main(maven_dir=MAVEN_DIR)
