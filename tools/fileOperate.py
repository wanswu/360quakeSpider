# -*- coding: utf-8 -*-
from datetime import datetime

fileName = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


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
            if dataTemp.get('domain') is not None:
                if dataTemp['domain'] == "":
                    f.write(f"{protocol}://{dataTemp['ip']}:{dataTemp['port']}\n")
                else:
                    f.write(f"{protocol}://{dataTemp['domain']}:{dataTemp['port']}\n")
            else:
                f.write(f"{protocol}://{dataTemp['ip']}:{dataTemp['port']}\n")



if __name__ == '__main__':
    print(readCookie())
