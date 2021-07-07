# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: cmd_helper.py
@time: 7/7/2021
@version:
"""
import os


def cmd_helper(cmd):
    # subprocess.check_output([cmd])
    # subprocess.Popen([cmd]).communicate()
    # subprocess.call(cmd)
    os.system(cmd)
    # tmp_file = open("tmp_file.sh", 'w')
    # tmp_file.write(cmd)
    # os.popen('./tmp_file.sh').read()
    # print(os.popen('./tmp_file.sh').read())
