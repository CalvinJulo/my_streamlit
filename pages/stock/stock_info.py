# -*-coding:utf-8 -*-

"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：python 3.9
# Description： 股票分析框架，
# 来源一：巨潮资讯 http://www.cninfo.com.cn
# 来源二：网易财经：如 http://quotes.money.163.com/f10/gsgg_000796,dqbg,4.html
"""

# 定期报告 http://www.cninfo.com.cn/new/disclosure/stock?tabName=data&orgId=gssh0600009&stockCode=600009&type=info#periodicReports

import requests
import time
import json

print('Beijing Time: ' + time.strftime("%Y-%m-%d %X"))
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'}


def query_from_cninfo(stock_code='000002', page_num=1):
    query_url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
    resp = requests.request(url=query_url, data={'searchkey': stock_code}, headers=headers, method='post')
    org_id = resp.json()['announcements'][0]['orgId']
    query = {
        'stock': f'{stock_code},{org_id}',  # stock: 300400,9900022164 ;000002,gssz0000002
        'tabName': 'fulltext',
        'pageNum': page_num,
        'pageSize': 30,
        'category': 'category_ndbg_szsh;category_scgkfx_szsh;',
        'isHLtitle': True,
    }
    response = requests.request(url=query_url, data=query, headers=headers, method='post', timeout=10)
    print(response.status_code)
    result = response.json()
    return result


def periodic_report(stock_code='000002'):
    report_lists = list()
    total_reports = 1
    num = 0
    while len(report_lists) != total_reports:
        num += 1   # 限制无限爬取
        if num > 10:
            print('Download Error')
            report_lists = []
            break
        total_pages = query_from_cninfo(stock_code=stock_code)['totalpages']+1
        for i in range(1, total_pages+1):
            result = query_from_cninfo(stock_code=stock_code, page_num=i)
            try:
                for j in result['announcements']:
                    report = dict()
                    report['code'] = j['secCode']
                    report['company'] = j['secName']
                    report['title'] = j['announcementTitle']
                    report['report'] = 'http://static.cninfo.com.cn/' + j['adjunctUrl']
                    report['reportSize'] = j['adjunctSize']
                    report_lists.append(report)
            except:
                print(f'Page{i} error')
            total_reports = result['totalAnnouncement']
    return report_lists


def stock_profile(stock_code='000002'):
    url = f'http://www.cninfo.com.cn/data20/companyOverview/getCompanyIntroduction?scode={stock_code}'
    profile_response = requests.request(url=url, headers=headers, method='get')
    profile_result = json.loads(profile_response.text)
    j = profile_result['data']['records'][0]["basicInformation"][0]
    i = profile_result['data']['records'][0]["listingInformation"][0]
    profile = {
        '公司名称': j['ORGNAME'],
        '英文名称': j['F001V'],
        '公司简称': j['ASECNAME'],
        '公司代码': j['ASECCODE'],
        '曾用简称': j['F002V'],
        '关联证券': {'B股': [j['BSECCODE'], j['BSECNAME']], 'H股': [j['HSECCODE'], j['HSECNAME']]},
        '所属市场': j['MARKET'],
        '所属行业': j['F032V'].split(','),
        '成立日期': j['F010D'],
        '上市日期': j['F006D'],
        '法人代表': j['F003V'],
        '总经理': j['F042V'],
        '公司董秘': j['F018V'],
        '邮政编码': j['F006V'],
        '注册地址': j['F004V'],
        '办公地址': j['F005V'],
        '联系电话': j['F013V'],
        '传真': j['F014V'],
        '官方网址': j['F011V'],
        '电子邮箱': j['F012V'],
        '每股面值(元)': i['F007N'],
        '首发价格(元)': i['F008N'],
        '首发募资净额(万元)': i['F028N'],
        '首发主承销商': i['F047V'].split(','),
        '入选指数': j['F044V'].split(','),
        '主营业务': j['F015V'],
        '经营范围': j['F016V'],
        '机构简介': j['F017V']
    }
    return profile


def stock_executives(stock_code='000002'):
    executives_url = f'http://www.cninfo.com.cn/data20/companyOverview/getCompanyExecutives?scode={stock_code}'
    executives_response = requests.request(url=executives_url, headers=headers, method='get')
    executives_result = json.loads(executives_response.text)['data']['records']
    executives = list()
    for i in executives_result:
        executive_url = f"http://www.cninfo.com.cn/new/executive/detail?stockcode={stock_code}&humanId={i['F001V']}"
        executive_response = requests.request(url=executive_url, headers=headers, method='get')
        j = json.loads(executive_response.text)
        executive = {
            '姓名': j['humanname'],
            '职务': i['F009V'].split(','),
            '年薪（万元）': i['F012N'],
            '持股数（股）': i['F005N'],
            '学历': j['education'],
            '出生年份': j['birtyday'],
            '性别': j['sex'],
            '国籍': j['nationality'],
            '曾任职上市公司情况': [{'公司': k['stockname'], '代码':k['stockcode'], '职位':k['job'],
                           '上任':time.strftime("%Y-%m-%d", time.localtime(k['servingdate']/1000)),
                           '离任':time.strftime("%Y-%m-%d", time.localtime(k['departdate']/1000)) if k['departdate'] != None else ''
                           } for k in j['jobonduty']],
            '个人简历': j['resume'],
            '上任时间': time.strftime("%Y-%m-%d", time.localtime(j['servingdate']/1000)),
            'ID': j['id'],
            'HumanID': j['humanid']
        }
        executives.append(executive)
    return executives


# Anniversary Stock Finance Indicator
def stock_indicators_data(stock_code='000002'):
    indicate_url = f'http://www.cninfo.com.cn/data20/financialData/getMainIndicators?scode={stock_code}&sign=1'
    indicators_year = json.loads(requests.request(url=indicate_url, headers=headers, method='get').content.decode("utf-8"))
    indicators_data = dict()
    for i in indicators_year['data']['records'][0]['year']:
        indicators_list = {'主要指标': '', '基本每股收益(元)': i['F004N'], '每股净资产(元)': i['F008N'],
                           '每股资本公积金(元)': i['F010N'], '营业总收入增长率(%)': i['F052N'], '加权净资产收益率(%)': i['F067N'],
                           '偿还能力指标': '', '流动比率': i['F042N'], '速动比率': i['F043N'], '资产负债比率(%)': i['F041N'],
                           '运营能力指标': '', '应收账款周转率(次)': i['F022N'], '存货周转率(次)': i['F023N'],
                           '流动资产周转率(次)': i['F029N'], '固定资产周转率(次)': i['F026N'], '总资产周转率(次)': i['F025N'],
                           '盈利能力指标': '', '营业利润率(%)': i['F011N'], '净利润率(%)': i['F017N'],
                           '毛利率(%)': i['F078N'], '总资产报酬率(%)': i['F016N'],
                           '发展能力指标': '', '营业收入增长率(%)': i['F052N'], '总资产增长率(%)': i['F056N'],
                           '营业利润增长率(%)': i['F058N'], '净利润增长率(%)': i['F053N'], '净资产增长率(%)': i['F054N']}
        indicators_data.update({'指标数据': list(indicators_list.keys())})
        indicators_data.update({i['ENDDATE']: list(indicators_list.values())})
    return indicators_data


# Anniversary Stock Finance Report
def stock_finance_data(stock_code='000002'):
    income_url = f'http://www.cninfo.com.cn/data20/financialData/getIncomeStatement?scode={stock_code}&sign=1'
    cash_flow_url = f'http://www.cninfo.com.cn/data20/financialData/getCashFlowStatement?scode={stock_code}&sign=1'
    balance_url = f'http://www.cninfo.com.cn/data20/financialData/getBalanceSheets?scode={stock_code}&sign=1'
    income_year = json.loads(requests.request(url=income_url, headers=headers, method='get').content.decode("utf-8"))
    cash_flow_year = json.loads(requests.request(url=cash_flow_url, headers=headers, method='get').content.decode("utf-8"))
    balance_year = json.loads(requests.request(url=balance_url, headers=headers, method='get').content.decode("utf-8"))
    i_values = [list(j.values()) for j in income_year['data']['records'][0]['year']]
    b_values = [list(j.values()) for j in balance_year['data']['records'][0]['year']]
    c_values = [list(j.values()) for j in cash_flow_year['data']['records'][0]['year']]
    finance_data = dict()
    for j in range(6):
        finance_list = {'利润表': '', '营业总收入': i_values[0][j], '营业总成本': i_values[1][j], '营业利润': i_values[2][j],
                        '利润总额': i_values[3][j], '所得税': i_values[4][j], '归属母公司净利润': i_values[5][j],
                        '资产负债表': '',
                        '资产类科目': '', '货币资金': b_values[1][j], '流动资产': b_values[2][j],
                        '非流动资产': b_values[3][j], '总资产': b_values[4][j],
                        '负债类科目': '', '流动负债': b_values[6][j], '长期借款': b_values[7][j],
                        '非流动负债': b_values[8][j], '总负债': b_values[9][j],
                        '股东权益类科目': '', '实收资本（或股本）': b_values[11][j],
                        '未分配利润': b_values[12][j], '所有者权益': b_values[13][j],
                        '现金流量表': '', '经营活动产生的现金流量净额': c_values[0][j],
                        '投资活动产生的现金流量净额': c_values[1][j], '筹资活动产生的现金流量净额': c_values[2][j]}
        finance_data.update({'财务数据(万元)': list(finance_list.keys())})
        year = list(income_year['data']['records'][0]['year'][0].keys())[j]
        if year != 'index':
            finance_data.update({f'{year}年度': list(finance_list.values())})
    return finance_data
