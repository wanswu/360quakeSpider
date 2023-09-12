# -*- coding: utf-8 -*-
import requests
from tqdm import tqdm
from datetime import datetime
import time

from .fileOperate import readCookie, writeDataFile, getStartDate


class requestInit:
    def __init__(self, searKey, size):
        """
        初始化变量
        :param searKey:搜索的语法
        :param size: 每页大小
        """
        self.data = {
            "latest": 'true',
            "ignore_cache": 'false',
            "shortcuts": ["635fcb52cc57190bd8826d09", "635fcbaacc57190bd8826d0b", "63734bfa9c27d4249ca7261c"],
            "query": searKey,
            "start": 0,
            "size": size,
            "device": {
                "device_type": "PC",
                "os": "Windows",
                "os_version": "10.0",
                "language": "zh_CN",
                "network": "4g",
                "browser_info": "Chrome（版本: 115.0.0.0&nbsp;&nbsp;内核: Blink）",
                "fingerprint": "50a2217e",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
                "date": f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}",
                "UUID": "da8f0570-47c6-5d6c-b8a3-a60b8084c937"
            },
        }
        self.api = 'https://quake.360.net/api/search/query_string/quake_service'
        self.hearders = {
            'Host': 'quake.360.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203',
            "Content-Type": "application/json",
            'Accept': 'application/json, text/plain, */*',
        }

        self.requests = requests.Session()

    def getTotalNum(self):
        """
        获取数据总量
        :return: 返回数据总量
        """
        self.hearders['Cookie'] = readCookie()
        resp = self.requests.post(url=self.api, headers=self.hearders, json=self.data)
        return resp.json()['meta']['pagination']['total']

    def getSearchData(self, start=0):
        """
        获取数据
        :param start:
        :return:
        """
        self.data['start'] = start
        resp = self.requests.post(url=self.api, headers=self.hearders, json=self.data)
        return resp.json()

    def run(self):
        allTotal = self.getTotalNum()
        print(f"共查到数据：{allTotal}条\n每次爬{self.data['size']}条\n准备开始爬取······")
        if allTotal > 100:
            data = datetime.now().strftime("%Y-%m-%d")
            # 开始时间是当前日期的前2两个月并且开启时间是 16:00:00
            self.data['start_time'] = data + ' 16:00:00'
            with tqdm(total=allTotal) as pbar:
                while allTotal != 0:
                    self.data['end_time'] = self.data['start_time'].split(' ')[0] + " 15:59:59"
                    self.data['start_time'] = getStartDate(self.data['start_time'].split(' ')[0]) + ' 16:00:00'
                    data = self.getSearchData()
                    pageTotal = data['meta']['pagination']['total']
                    if pageTotal > self.data['size']:
                        for _ in range(0, pageTotal, self.data['size']):
                            writeDataFile(self.getSearchData(_))
                            pbar.update(self.data['size'])  # 更新进度条
                    else:
                        writeDataFile(data)
                        pbar.update(pageTotal)  # 更新进度条
                    allTotal -= data['meta']['pagination']['total']
                    time.sleep(1)
        else:
            for _ in tqdm(range(0, allTotal, self.data['size'])):
                writeDataFile(self.getSearchData(_))
                time.sleep(0.5)
