#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

FernFlower_PATH = 'tools/fernflower.jar'

FASTJSON_BLACK="""
org.apache.commons.collections4.comparators
org.python.core
org.apache.tomcat
org.apache.xalan
javax.xml
org.springframework.
org.apache.commons.beanutils
org.apache.commons.collections.Transformer
org.codehaus.groovy.runtime
java.lang.Thread
javax.net.
com.mchange
org.apache.wicket.util
java.util.jar.
org.mozilla.javascript
java.rmi
java.util.prefs.
com.sun.
java.util.logging.
org.apache.bcel
java.net.Socket
org.apache.commons.fileupload
org.jboss
org.hibernate
org.apache.commons.collections.functors
org.apache.myfaces.context.servlet
java.net.URL
junit.
org.apache.ibatis.datasource
org.osjava.sj.
org.apache.log4j.
org.logicalcobwebs.
org.apache.logging.
org.apache.commons.dbcp
com.ibatis.sqlmap.engine.datasource
org.jdom.
org.slf4j.
javassist.
oracle.net
org.jaxen.
java.net.InetAddress
java.lang.Class
com.alibaba.fastjson.annotation
org.apache.cxf.jaxrs.provider.
ch.qos.logback.
net.sf.ehcache.transaction.manager.
meituan
dianping
sankuai
maoyan
"""
FASTJSON_BLACK_LIST = FASTJSON_BLACK.strip().split('\n')

# maven 目录
MAVEN_DIR = '%s/.m2/repository/' % os.path.expanduser('~')

# 临时文件存储
SOURCE_DIR = '/tmp/maven/source/'
if os.path.isfile(SOURCE_DIR):
    os.mkdir(SOURCE_DIR)

# 结果存储
RESULT_FILE = 'logs/result.txt'
