#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import subprocess
import threading
import logging

class RunCmd(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = subprocess.Popen(self.cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            logging.debug('kill pid')
            self.p.terminate()  # use self.p.kill() if process needs a kill -9
            self.join()
