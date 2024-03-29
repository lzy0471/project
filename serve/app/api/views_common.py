# -*- coding: utf-8 -*-
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import tornado.web

from app.common.ip2Addr import ip2addr
from app.configs import mongodb_configs
from pymongo import MongoClient  # mongodb的客户端连接工具
from werkzeug.datastructures import MultiDict


class CommonHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(1000)  # 定义线程池

    #前缀地址
    @property
    def site_url(self):
        return 'http://127.0.0.1:8003'

    # 客户端向服务器端发送的数据进行处理
    # json转化为字典

    # 这里是None
    @property
    def md(self):
        # 集成mongodb
        md = MongoClient(
            host=mongodb_configs['db_host'],
            port=mongodb_configs['db_port']
        )

        return md


    @property
    def params(self):
        data = self.request.body
        # 包含字节类型，转化为python数据类型
        # 由于小程序端提交数据类型是json字符串
        # json字符串在后端进行获取的时候是字节类型，解码为字符串类型
        # 将json字符串转化为字典类型
        data = {
            k: v
            for k, v in json.loads(data.decode('utf-8')).items()
        }
        return data

    @property
    def dt(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 返回一个时间



    # 公共参数
    def common_params(self):
        data = dict(
            createAdt=self.dt,
            ip=self.request.remote_ip,
            addr=ip2addr(self.request.remote_ip)['region'].decode('utf-8'),
            headers=dict(self.request.headers)
        )
        return data
    #ajax异步提交数据
    @property
    def ajax_params(self):
        data = self.request.arguments
        data = {
            k:list(
                map(
                    lambda val:str(
                        val,encoding='utf-8'
                    ),
                    v
                )
            )
            for k, v in data.items()
        }
        return data
    #表单数据
    @property
    def form_params(self):
        return MultiDict(self.ajax_params)