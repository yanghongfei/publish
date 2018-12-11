#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/7 10:24
# @Author  : Fred Yang
# @File    : cmdb_api.py
# @Role    : CMDB API


import pyotp
import requests
import json


class CMDB_API():
    def __init__(self):
        self.url = 'http://gw.domain.com'
        self.user = 'user'
        self.pwd = 'passwd'
        self.key = 'key'

    @property
    def get_mfa(self):
        t = pyotp.TOTP(self.key)
        return t.now()

    def login(self):
        headers = {"Content-Type": "application/json"}
        params = {"username": self.user, "password": self.pwd, "dynamic": self.get_mfa}
        result = requests.post('%s/accounts/login/' % self.url, data=json.dumps(params), headers=headers)
        ret = json.loads(result.text)
        if ret['code'] == 0:
            return ret['auth_key']
        else:
            print(ret)
            print(ret['msg'])
            exit(1)

    def get_ec2_info(self, publish_host_api):
        """
        获取主机信息
        :param publish_host_api: 前端传来
        :return:
        """

        token = self.login()
        # res = requests.get('%s/cmdb/api/cmdb/server_list/' % self.url, params=params, cookies=dict(auth_key=token))
        res = requests.get('{}'.format(publish_host_api), cookies=dict(auth_key=token))
        print('CMDB_API request Status:{}'.format(res.status_code))
        # ret = str(res.content,'utf-8') py3
        ret = str(res.text)
        data = json.loads(ret)
        return data
