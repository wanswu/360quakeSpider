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
            'start_time': "2015-08-07 16:00:00",
            "end_time": "2022-09-30 15:59:59",
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
                "date": "2023/8/21 14:36:44",
                "UUID": "da8f0570-47c6-5d6c-b8a3-a60b8084c937"
            },
            "a34lrc0gjl9": "="
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
        将数据写入文件中
        :param data:
        :return:
        """
        with open(f'{fileName}.txt', 'a+', encoding='utf8') as f:
            f.write(data + "\n")

    def getTotalNum(self):
        """
        获取数据总量
        :return: 返回数据总量
        """
        resp = self.requests.post(url=self.api, headers=self.hearders, json=self.data)
        return resp.json()['meta']['pagination']['total']

    def getSearchData(self, start):
        """
        获取数据
        :param start:
        :return:
        """
        self.data['start'] = start
        resp = self.requests.post(url=self.api, headers=self.hearders, json=self.data)
        allData = resp.json()
        return allData['data']

    def calculate_months_before(self, start_time_str):
        start_time_str = datetime.strptime(start_time_str, '%Y-%m-%d')
        # 计算三个月的时间间隔
        three_months = timedelta(days=60)  # 假设每月30天

        # 计算之前三个月的时间
        before_time = start_time_str - three_months
        return before_time.strftime('%Y-%m-%d')

    def run(self):
        self.hearders['Cookie'] = self.readCookie()
        allTotal = self.getTotalNum()
        num = 0
        if allTotal > 10000:
            total = self.getTotalNum()
            data = datetime.now().strftime("%Y-%m-%d")
            self.data['start_time'] = self.calculate_months_before(data) + ' 16:00:00'
            self.data['end_time'] = data + ' 15.59.59'
            print(self.data['start_time'])
            print(self.data['end_time'])
            num += total
        # print(f"共查到数据：{total}条\n每次爬{self.data['size']}条\n准备开始爬取······")
        # if total >= 10000:
        #     total = 10000
        # for _ in tqdm(range(0, total, self.data['size'])):
        #     for dataTemp in self.getSearchData(_):
        #         if len(dataTemp['service']['http']['http_load_url']) == 0:
        #             continue
        #         else:
        #             protocol = "https" if "ssl" in dataTemp['service']['name'] else "http"
        #             self.writeDataFile(f"{protocol}://{dataTemp['ip']}:{dataTemp['port']}")
        #     time.sleep(0.5)


if __name__ == '__main__':
    defaultSearchKey = ' AND service: "http" AND is_domain:"false"'
    # searKey = input('请输入查询语法：(默认去除cdn、蜜罐、无效请求)\n') + defaultSearchKey
    searKey = 'city:"宝鸡" AND favicon: "e05b47d5ce11d2f4182a964255870b76"' + defaultSearchKey
    # print(searKey)
    safe = safeSearch(searKey=searKey, size=10)
    safe.run()
