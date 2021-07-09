# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Wang Zhiyi
@file: cmd_helper.py
@time: 7/7/2021
@version:
"""

_servers = ['spark-797d5ccdb-2jmdw', 'spark-797d5ccdb-4sq79', 'spark-797d5ccdb-6hsdc', 'spark-797d5ccdb-72z2j',
            'spark-797d5ccdb-9qz5w', 'spark-797d5ccdb-c56g9', 'spark-797d5ccdb-csq2m', 'spark-797d5ccdb-fjmbr',
            'spark-797d5ccdb-h2hcq', 'spark-797d5ccdb-ht7vz', 'spark-797d5ccdb-kvsrm', 'spark-797d5ccdb-l7txm',
            'spark-797d5ccdb-ln2xr', 'spark-797d5ccdb-m6ctm', 'spark-797d5ccdb-m92qw', 'spark-797d5ccdb-n2sr7',
            'spark-797d5ccdb-p86qx', 'spark-797d5ccdb-ph9lc', 'spark-797d5ccdb-pzz6s', 'spark-797d5ccdb-r78mv',
            'spark-797d5ccdb-rjb6h', 'spark-797d5ccdb-s2hb2', 'spark-797d5ccdb-s7fw6', 'spark-797d5ccdb-s8jdd',
            'spark-797d5ccdb-vp48k', 'spark-797d5ccdb-vt9c7', 'spark-797d5ccdb-x84dm', 'spark-797d5ccdb-xbwtr',
            'spark-797d5ccdb-xwtgf', 'spark-797d5ccdb-zgsg4', 'spark-797d5ccdb-zsk59']

import os

import paramiko

_ssh_client = paramiko.SSHClient()
_key = paramiko.AutoAddPolicy()
_ssh_client.set_missing_host_key_policy(_key)
_sftp_client = None


def _get_connect(server):
    _ssh_client.connect('{}'.format(server), 22, 'hduser', '', timeout=5)


def _execute_cmd(cmd):
    stdin, stdout, stderr = _ssh_client.exec_command(str(cmd))
    print(stdout.read())


def _close_connect():
    _ssh_client.close()


def _open_sftp(server):
    _get_connect(server)
    global _sftp_client
    _sftp_client = _ssh_client.open_sftp()


def execute_remote_cmd(server, cmd):
    _get_connect(str(server))
    _execute_cmd(cmd)
    _close_connect()


def synchronize_file(local, remote, syn_type="folder"):
    for server in _servers:
        if syn_type == "folder":
            try:
                os.system("scp -rf {} {}:{}".format(local, str(server), remote))
                print(str(server))
            except Exception:
                print("Folder already exists.")
                pass


def help_start_generator(container_count=3):
    # for server in _servers[:5]:
    #     cmd = 'rm -rf /home/hduser/fraudiscern'
    #     execute_remote_cmd(str(server), cmd)
    # synchronize_file("/home/hduser/fraudiscern", "/home/hduser/fraudiscern")
    # cmd = "ls"
    # _execute_cmd(cmd)
    for server in _servers[:container_count]:
        print("start server {}".format(str(server)))
        # cmd_install_python_packages = "pip install -r packages.txt"
        cmd_submit_generator = "spark-submit --master yarn /home/hduser/fraudiscern/source/utils/stress_test_producer.py --py-files /home/hduser/fraudiscern/source/utils/dependencies_v1.zip"
        execute_remote_cmd(str(server), cmd_submit_generator)


if __name__ == '__main__':
    help_start_generator(container_count=2)
