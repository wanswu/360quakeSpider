"""
版本：0.0.1
目前只会爬取http/https
网页最大查询为10,000条
"""
import requests
import time
from tqdm import tqdm

# 格式化时间戳为可读的时间字符串
formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())


class safeSearch:
    def __init__(self, searKey, cookie):
        self.data = {
            "latest": 'true',
            "ignore_cache": 'false',
            "shortcuts": ["635fcb52cc57190bd8826d09", "635fcbaacc57190bd8826d0b", "63734bfa9c27d4249ca7261c"],
            "query": searKey,
            "start": 0,
            "size": 10,
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
            'Cookie': cookie
        }
        self.requests = requests.Session()
        resp = \
            self.requests.post(url=self.api, headers=self.hearders, json=self.data).json()[
                'meta'][
                'pagination']['total']
        self.total = resp

    def getSearchData(self, start):
        self.data['start'] = start
        resp = self.requests.post(url=self.api, headers=self.hearders, json=self.data)
        allData = resp.json()
        for i in allData['data']:
            data = i['service']['http']['http_load_url'][0]
            self.writeFile(data)

    def writeFile(self, data):
        with open(f'{formatted_time}.txt', 'a+', encoding='utf8') as f:
            f.write(data + "\n")

    def __del__(self):
        self.requests.close()

    def run(self):
        print(f"""
共查到数据：{self.total}条
准备开始爬取
""")
        for i in tqdm(range(0, self.total, 10)):
            self.getSearchData(i)


if __name__ == '__main__':
    cookie = input('请输入你的cookie：')
    searKey = input('请输入查询语法：(最好带上service: "http")\n')
    safe = safeSearch(searKey=searKey, cookie=cookie)
    safe.run()
