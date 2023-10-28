# -*-coding:utf-8 -*-

"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：python 3.9
# Description： 股票分析框架，同花顺 https://www.10jqka.com.cn
"""


import pandas as pd
import time


print('Beijing Time: ' + time.strftime("%Y-%m-%d %X"))

# Excel版
# 主要指标 http://basic.10jqka.com.cn/api/stock/export.php?export=main&type=year&code=002707
# 资产负债表 http://basic.10jqka.com.cn/api/stock/export.php?export=debt&type=year&code=002707
# 利润表 http://basic.10jqka.com.cn/api/stock/export.php?export=benefit&type=year&code=002707
# 现金流量表 http://basic.10jqka.com.cn/api/stock/export.php?export=cash&type=year&code=002707
# 网页加载版本
# http://basic.10jqka.com.cn/api/stock/finance/002707_main.json
# http://basic.10jqka.com.cn/api/stock/finance/002707_debt.json
# http://basic.10jqka.com.cn/api/stock/finance/002707_benefit.json
# http://basic.10jqka.com.cn/api/stock/finance/002707_cash.json


# 获得数据Excel的url，手动保存本地并改为CSV格式
def get_excel_url(code='000001', export='main', type_='year'):
    # export 参数值: 主要指标main, 资产负债表debt, 利润表benefit，现金流量表cash
    # type_ 参数值： 报告report， 年度year， 季度simple
    url = 'http://basic.10jqka.com.cn/api/stock/export.php?export=' + export + '&type=' + type_ + '&code=' + code
    print(url)
    return url


def get_csv_data(path='002707_main_year.csv'):
    df = pd.read_csv(path)
    df.columns = list(df.loc[0])
    df.index = list(df.iloc[:, 0])
    df = df.iloc[1:len(df) - 1, 1:]
    return df
