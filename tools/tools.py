# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

fileName = datetime.now().strftime("%Y-%m-%d_%H:%M")


def readCookie():
    """
    读取cookie
    :return: 返回cookie
    """
    try:
        with open('config.ini', 'r', encoding='utf8') as f:
            return f.read()
    except:
        with open('config.ini', 'w', encoding='utf8') as f:
            print('将cookie写入config.ini中')
            exit(0)
    finally:
        f.close()


def writeDataFile(data):
    """
    将数据写入文件中，接受的值为返回的所有的数据
    :param data:
    :return:
    """
    for dataTemp in data['data']:
        protocol = "https" if "ssl" in dataTemp['service']['name'] else "http"
        with open(f'./result/{fileName}.txt', 'a+', encoding='utf8') as f:
            f.write(f"{protocol}://{dataTemp['ip']}:{dataTemp['port']}\n")


def getStartDate(start_time_str):
    start_time_str = datetime.strptime(start_time_str, '%Y-%m-%d')
    # 计算三个月的时间间隔
    three_months = timedelta(days=60)  # 假设每月30天
    # 计算之前三个月的时间
    before_time = start_time_str - three_months
    return before_time.strftime('%Y-%m-%d')


if __name__ == '__main__':
    print(readCookie())
