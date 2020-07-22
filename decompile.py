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


def main(maven_dir=MAVEN_DIR):
    '''
    :return:
    '''
    print('maven_dir: %s' % maven_dir)
    jar_files = get_file_list(maven_dir)
    print('total: %s' % len(jar_files))

    for jar_file in jar_files:
        try:
            logging.info(jar_file)
            source_dir = decomplier(jar_file)

        except Exception as e:
            logging.error(e, exc_info=True)


def usage():
    print('decompile jars to classes')
    print('usage: python %s [maven_dir]' % __file__)
    exit(1)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        usage()

    elif len(sys.argv) == 2:
        if os.path.isdir(sys.argv[1]):
            main(maven_dir=sys.argv[1])

    elif len(sys.argv) == 1:
        main(maven_dir=MAVEN_DIR)

