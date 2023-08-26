from datetime import datetime, timedelta


def calculate_months_before(start_time_str):
    start_time_str = datetime.strptime(start_time_str, '%Y-%m-%d')
    # 计算三个月的时间间隔
    three_months = timedelta(days=60)  # 假设每月30天

    # 计算之前三个月的时间
    before_time = start_time_str - three_months
    return before_time


start_time_str = datetime.now().strftime("%Y-%m-%d")
before_time = calculate_months_before(start_time_str)

print(f"开始时间：{start_time_str}\n结束时间：{before_time.strftime('%Y-%m-%d')}")
