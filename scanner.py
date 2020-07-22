#!/usr/bin/env python
# -*- coding: UTF-8 -*-


"""
Created on 2019/8/7 

@author: tmy
"""
from utils.lib import *
from utils.scan_jndi import scan_jndi_gadgate, clean
from settings import *
import logging
from pprint import pprint, pformat

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    filename='logs/scanner.log'
                )

def main():
    '''
    :return:
    '''
    jar_files = get_file_list(MAVEN_DIR)
    print('total: %s' % len(jar_files))
    logging.warning('total jars: %s' % len(jar_files))

    for jar_file in jar_files:
        try:
            logging.info(jar_file)
            source_dir = decomplier(jar_file)
            class_files = get_java_file(source_dir)
            logging.warning('total class: %s' % len(class_files))
            if not jar_file:
                continue
            for class_file in class_files:
                try:
                    logging.info('scanning',jar_file,class_file)
                    if class_file:
                        scan_jndi_gadgate(class_file)
                except Exception as e:
                    logging.error(e,exc_info=True)

        except Exception as e:
            logging.error(e,exc_info=True)

    scanner_list = read_file(RESULT_FILE)
    results = clean(scanner_list)
    logging.warning(pformat(results))

if __name__ == '__main__':
    main()
