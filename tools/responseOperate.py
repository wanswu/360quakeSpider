# -*- coding: utf-8 -*-
from datetime import datetime, timedelta


def getStartDate(start_time_str):
    """
    计算90天之前的时间，作为开始的时间
    :param start_time_str:
    :return:
    """
    start_time_str = datetime.strptime(start_time_str, '%Y-%m-%d')
    # 计算三个月的时间间隔
    three_months = timedelta(days=60)  # 假设每月30天
    # 计算之前三个月的时间
    before_time = start_time_str - three_months
    return before_time.strftime('%Y-%m-%d')


if __name__ == '__main__':
    print('test')
