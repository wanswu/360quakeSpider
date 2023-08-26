"""
版本：0.0.3
目前只会爬取http/https
网页最大查询为10,000条
"""
import requests
import time
from tqdm import tqdm
from datetime import datetime, timedelta

fileName = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


class safeSearch:
    def __init__(self, searKey, size):
        """
        初始化变量
        :param searKey:
        :param size:
        """
        # 还有两个参数未使用一个是
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
                "date": f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}",
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

    def __del__(self):
        self.requests.close()

    def readCookie(self):
        """
        读取cookie
        :return: 返回cookie
        """
        try:
            with open('../config.ini', 'r', encoding='utf8') as f:
                return f.read()
        except:
            with open('../config.ini', 'w', encoding='utf8') as f:
                print('将cookie写入config.ini中')
                exit(0)

    def writeDataFile(self, data):
        """
        将数据写入文件中，接受的值为返回的所有的数据
        :param data:
        :return:
        """
        for dataTemp in data['data']:
            protocol = "https" if "ssl" in dataTemp['service']['name'] else "http"
            with open(f'../result/{fileName}.txt', 'a+', encoding='utf8') as f:
                f.write(f"{protocol}://{dataTemp['ip']}:{dataTemp['port']}\n")

    def getTotalNum(self):
        """
        获取数据总量
        :return: 返回数据总量
        """
        self.hearders['Cookie'] = self.readCookie()
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
        print(resp.request.body)
        return resp.json()

    def getStartDate(self, start_time_str):
        print(start_time_str)
        start_time_str = datetime.strptime(start_time_str, '%Y-%m-%d')
        # 计算三个月的时间间隔
        three_months = timedelta(days=60)  # 假设每月30天

        # 计算之前三个月的时间
        before_time = start_time_str - three_months
        return before_time.strftime('%Y-%m-%d')

    def run(self):
        allTotal = self.getTotalNum()
        print(f"共查到数据：{allTotal}条\n每次爬{self.data['size']}条\n准备开始爬取······")
        num = 0
        if allTotal > 10:
            data = datetime.now().strftime("%Y-%m-%d")
            # 开始时间是当前日期的前2两个月并且开启时间是 16:00:00
            self.data['start_time'] = self.getStartDate(data) + ' 16:00:00'
            # 结束时间是当前日期并且结束时间为 15:59:59
            self.data['end_time'] = data + ' 15:59:59'
            dataTemp = self.getSearchData()
            self.writeDataFile(dataTemp)
            allTotal -= dataTemp['meta']['pagination']['total']
            while allTotal != 0:
                # 结束时间为上一次的结束时间
                self.data['end_time'] = self.data['start_time'].split(' ')[0] + " 15:59:59"
                # 开始时间为上一次开始时间的前2个月的时间
                self.data['start_time'] = self.getStartDate(self.data['start_time'].split(' ')[0]) + ' 16:00:00'
                data = self.getSearchData()
                self.writeDataFile(data)
                allTotal -= data['meta']['pagination']['total']


        else:
            for _ in tqdm(range(0, allTotal, self.data['size'])):
                self.writeDataFile(self.getSearchData(_))
                time.sleep(0.5)


if __name__ == '__main__':
    defaultSearchKey = ' AND service: "http" AND is_domain:"false"'
    # searKey = input('请输入查询语法：(默认去除cdn、蜜罐、无效请求)\n') + defaultSearchKey
    searKey = 'city:"宝鸡" AND favicon: "e05b47d5ce11d2f4182a964255870b76"' + defaultSearchKey
    print(searKey)
    safe = safeSearch(searKey=searKey, size=10)
    safe.run()
