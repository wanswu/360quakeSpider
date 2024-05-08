# -*- coding: utf-8 -*-
import requests
from tqdm import tqdm
from datetime import datetime
import time

from .fileOperate import readCookie, writeDataFile
from .responseOperate import getStartDate
requests.packages.urllib3.disable_warnings()

class requestInit:
    def __init__(self, searKey, size):
        """
        初始化变量
        :param searKey:搜索的语法
        :param size: 每页大小
        """
        self.data = {
            "latest": 'true',
            "ignore_cache": 'true',
            "shortcuts": [],
            "start": 0,
            "size": size,
            "device": {
                "device_type": "PC",
                "os": "Mac OS",
                "os_version": "10.15.7",
                "language": "zh_CN",
                "network": "5g",
                "browser_info": "Chrome（版本: 120.0.0.0&nbsp;&nbsp;内核: Blink）",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "date": f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}",

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
        resp = self.requests.post(url=self.api, headers=self.hearders, json=self.data,verify=False)
        return resp.json()['meta']['pagination']['total']

    def getSearchData(self, start=0):
        """
        获取数据
        :param start:
        :return:
        """
        self.data['start'] = start
        resp = self.requests.post(url=self.api, headers=self.hearders, json=self.data)
        self.requests.close()
        return resp.json()

    def run(self):
        allTotal = self.getTotalNum()
        print(f"共查到数据：{allTotal}条\n每次爬{self.data['size']}条\n准备开始爬取······")
        # 如果总数据超过了1w那么就分批查询
        if allTotal > 10000:
            data = datetime.now().strftime("%Y-%m-%d")
            # 开始时间是当前日期的前2两个月并且开启时间是 16:00:00
            self.data['start_time'] = data + ' 16:00:00'
            with tqdm(total=allTotal+1) as pbar:
                # 循环爬取，每次向前推60天
                while allTotal != 0:
                    # 结束直接为上次的开始时间
                    self.data['end_time'] = self.data['start_time'].split(' ')[0] + " 15:59:59"
                    # 获取前60天的时间
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
                    time.sleep(5)
        else:
            for _ in tqdm(range(0, allTotal, self.data['size'])):
                writeDataFile(self.getSearchData(_))
                time.sleep(0.5)
