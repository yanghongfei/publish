#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/5 10:29
# @Author  : Fred Yang
# @File    : get_publish_info.py
# @Role    : 获取发布信息写文件


import os
import sys
import json
from publish_api import Publish_API
from public import lock_json
import fire


def data_save(file_name, data):
    """
    :param data: 通过API取到发布配置信息
    :param file_name: 配置信息存储文件路径
    :return:
    """
    lock_json(sys.argv[0])
    if not os.path.exists(file_name):
        os.system("echo {} > %s" % file_name)

    try:
        f = open(file_name, 'w', encoding='utf-8')
        jsObj = json.dumps(data)
        f.write(jsObj)
        f.close()
        print('[INFO]: Publish info has been written :{}'.format(file_name))
    except Exception as e:
        print(e)
        print('[Error]: Publish info write falid')


def get_publish_data(flow_id):
    file_name = '/tmp/publish_{}.json'.format(flow_id)
    if not os.path.exists(file_name):
        print('[Error]: Not Fount config file... ')
        exit(400)
    else:
        f = open(file_name, 'r', encoding='utf-8')
        for line in f:
            ret = json.loads(line)
            for data in ret:
                return data

def get_all_hosts():
    now_all_hosts = {'172.16.0.20': ['22', 'root', 'None'], '172.16.0.228': ['22', 'root', '123456'],
                     '172.16.0.101': ['22', 'root', '1']}
    all_hosts = []
    for hosts_key in now_all_hosts.keys():
        hosts_value = now_all_hosts[hosts_key]
        hosts_data = {
            'ip': hosts_key,
            'port': hosts_value[0],
            'user': hosts_value[1],
            'password': hosts_value[2]
        }
        all_hosts.append(hosts_data)
    return all_hosts


def main(publish_name, flow_id):
    """
    :param publish_name: 发布应用的名称
    :param flow_id: 订单ID
    :return:
    """
    file_name = '/tmp/publish_{}.json'.format(flow_id)
    obj = Publish_API()
    data = obj.get_publish_name_info(publish_name)
    data_save(file_name, data)


if __name__ == '__main__':
    fire.Fire(main)
