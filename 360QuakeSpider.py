# -*- coding: utf-8 -*-
from tools.requestDataInit import requestInit


def main():
    defaultSearchKey = ' AND service: "http"'
    searKey = input('请输入查询语法：(默认去除cdn、蜜罐、无效请求)\n') + defaultSearchKey
    # searKey = 'city:"宝鸡"' + defaultSearchKey
    print(f'你输入的语法为：{searKey}')
    requestInit(searKey=searKey, size=100).run()
    print('爬取完成')


if __name__ == '__main__':
    main()
