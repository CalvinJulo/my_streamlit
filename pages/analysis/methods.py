# -*-coding:utf-8 -*-


def method():
    method_list = ['5W2H分析', '逻辑树分析', '行业分析PEST', '行业分析SWOT', '多维度拆解分析',
                  '对比分析', '假设检验分析', '相关分析', '群组分析',
                  'RFM分析', 'AARRR模型分析', '漏斗分析']
    f = method_list.copy()
    return f


def wh_analysis():
    method_title = '5W2H分析方法'
    method_capt = ['5W：what（是什么）、when（何时）、where（何地）、why（为什么）、who（是谁）','2H：how（怎么做）、how much（多少钱）',
               '5W2H分析方法对复杂的商业问题不适用。因为复杂的商业问题一般是由多个原因引起的。']
    method_cases = {
        'case1': {'title': '案例一: 如何设计一款产品？',
                 'context': ['what（是什么）：这是什么产品？', 'when（何时）：什么时候需要上线？',
                  'where（何地）：在哪里发布这些产品？', 'why（为什么）：用户为什么需要它？',
                  'who（是谁）：这是给谁设计的', 'how（怎么做）：这个产品需要怎么运作？',
                  'how much（多少钱）：这个产品里有付费功能吗？价格是多少？']},
        'case2': {'title':'案例二: 设计一款App的调查问卷，如何设计问卷上的问题？',
                  'context':['what（是什么）：你用这款App做什么事情？', 'when（何时）：你通常在什么时间使用这款App？',
                  'where（何地）：你会在什么场景使用这款App？', 'why（为什么）：你为什么选择这款App？',
                  'who（是谁）：如果你觉得你喜欢这个产品，你会推荐给谁？', 'how（怎么做）：你觉得我们需要加入什么功能才是比较新颖的？',
                  'how much（多少钱）：如果你认为这个App对你有帮助，你会花多少钱去购买App里的服务？']}}
    return method_title, method_capt, method_cases


def logictree_analysis():
    method_title = '逻辑树分析方法'
    method_capt = '逻辑树分析方法是把复杂问题拆解成若干个简单的子问题，然后像树枝那样逐步展开'
    method_cases = {
        'feimi': {'title': '费米问题',
                 'context': ['地球的周长是多少？', '芝加哥有多少钢琴调音师？', '胡同口的煎饼摊子一年能卖多少个煎饼？',
                  '一辆公交车里能装下多少个乒乓球？', '一个正常成年人有多少根头发？'],
                  'intro': ['费米问题是在科学研究中用来做量纲分析、估算和清晰地验证一个假设的估算问题。命名来自美国科学家恩利克·费米。',
                            '这类问题通常包括关于给定限定信息的有可能计算的数量的猜想的验证。',
                            '这类问题能区分两类人：一类是具有文科思维的人，擅长赞叹和模糊想象，主要依靠的是第一反应和直觉，例如小孩；另一类是具有理科思维的人，擅长通过逻辑推理、分析解决具体问题。'],},
        'graphviz_chart': '''
            digraph {
                问题 -> 子问题A
                问题 -> 子问题B
                问题 -> 子问题C
                问题 -> 子问题D
                子问题A -> 孙问题A
                子问题A -> 孙问题B
                子问题A -> 孙问题C
                子问题C -> 孙问题D
                子问题C -> 孙问题E
            }
        '''}
    return method_title, method_capt, method_cases


# '行业分析方法' (Industry Analysis Method)
def industry_pest_analysis():
    method_title = 'PEST分析方法'
    method_capt = ('PEST分析是指宏观环境的分析，P是政治(politics)，E是经济(economy)，S是社会(society)，T是技术(technology)。'
                   '在分析一个企业集团所处的背景的时候，通常是通过这四个因素来分析企业集团所面临的状况。')
    method_cases = {
        'Political Factors':'政治环境主要包括政治制度与体制，政局，政府的态度等；法律环境主要包括政府制定的法律、法规。',
        'Economic Factors':'构成经济环境的关键战略要素：GDP、利率水平、财政货币政策、通货膨胀、失业率水平、居民可支配收入水平、汇率、能源供给成本、市场机制、市场需求等。',
        'Sociocultural Factors':'影响最大的是人口环境和文化背景。人口环境主要包括人口规模、年龄结构、人口分布、种族结构以及收入分布等因素。',
        'Technological Factors':'技术环境不仅包括发明，而且还包括与企业市场有关的新技术、新工艺、新材料的出现和发展趋势以及应用背景。'}
    return method_title, method_capt, method_cases

def industry_swot_analysis():
    method_title = 'SWOT分析方法'
    method_capt = '技术环境不仅包括发明，而且还包括与企业市场有关的新技术、新工艺、新材料的出现和发展趋势以及应用背景。'
    method_cases = {
        'S （strengths）':'组织机构的内部因素，具体包括：有利的竞争态势；充足的财政来源；良好的企业形象；技术力量；规模经济；产品质量；市场份额；成本优势；广告攻势等。',
        'W （weaknesses）':'组织机构的内部因素，具体包括：设备老化；管理混乱；缺少关键技术；研究开发落后；资金短缺；经营不善；产品积压；竞争力差等。',
        'O （opportunities）' :'组织机构的外部因素，具体包括：新产品；新市场；新需求；外国市场壁垒解除；竞争对手失误等。',
        'T （threats）':'组织机构的外部因素，具体包括：新的竞争对手；替代产品增多；市场紧缩；行业政策变化；经济衰退；客户偏好改变；突发事件等。'
    }
    return method_title, method_capt, method_cases


# '多维度拆解分析方法' (Multidimensional Breakdown Analysis Method)
def multidimensional_analysis():
    method_title = '多维度拆解分析方法'
    method_capt = ['将整体通过不同维度拆解成不同部分，分别进行考察',
               '要注意“辛普森悖论”，也就是在有些情况下，考察数据整体和考察数据的不同部分，会得到相反的结论。使用多维度拆解分析方法，可以防止“辛普森悖论',
               ]
    method_cases = {
        '从指标构成来拆解':['新用户销售额=新用户数×转化率×新用户客单价','老用户销售额=老用户数×复购率×老用户客单价'],
        '从业务流程来拆解': {'用户购买的业务流程': [
            '第1步，看到渠道的广告；','第2步，被广告吸引进入店铺；','第3步，在店铺选择感兴趣的商品；','第4步，选择好商品，最终决定购买。']}}
    return method_title, method_capt, method_cases


# '对比分析方法' (Comparative Analysis Method)
def comparative_analysis():
    method_title = '对比分析方法'
    method_capt = []
    method_cases = {
        '和谁比': {'和自己比':'历史业绩比较','和行业比':'同行比较'},
        '怎么比': {'数据整体的大小':'平均值, 中位数,或者某个业务指标','数据整体的波动':'变异系数(标准差除以平均值)',
                   '趋势变化':'时间折线图,环比,同比'},
        'A/B测试':'context'}
    return method_title, method_capt, method_cases


# '假设检验分析方法' (Hypothesis Testing Analysis Method)
def hypothesis_analysis():
    method_title = '假设检验分析方法'
    method_capt = ['假设检验分析方法就是逻辑推理，是一种使用数据来做决策的过程。它分为3步：提出假设，收集证据，得出结论。',
                   '客观地提出假设，同时防止遗漏假设',
                   '结论不是主观猜想出来的，不能是“我猜、我觉得、我认为、我感觉”，而是要依靠找到的证据去证明结论']
    method_cases = {'企业管理':['从用户、产品、竞品这3个维度提出假设','从4P营销理论提出假设','从业务流程提出假设。']}
    return method_title, method_capt, method_cases

# '相关分析方法' (Correlation Analysis Method)
def correlation_analysis():
    method_title = '相关分析方法'
    method_capt = ['研究两种或者两种以上数据之间有关系', '需要注意的是相关关系不等于因果关系',
                   '要用到单变量控制法，也就是控制其他因素不变，只改变其中一个因素，然后观察这个因素对实验结果的影响。']
    method_cases = {'分析工具':['相关系数','散点图']}
    return method_title, method_capt, method_cases


# '群组分析方法' (Cluster Analysis Method)
def cluster_analysis():
    method_title = '群组分析方法'
    method_capt = '群组分析方法”是按某个特征，将数据分为不同的组，然后比较各组的数据。'
    method_cases = {'案例': ['视频平台用户流失分析','推特用户留存分析','金融行业逾期分析']}
    return method_title, method_capt, method_cases



# 'RFM分析方法' (RFM Analysis Method)
def rfm_analysis():
    method_title = 'RFM分析方法'
    method_capt = {'RFM缩写':'RFM是3个指标的缩写：最近1次消费时间间隔（Recency）、消费频率（Frequency）、消费金额（Monetary',
                   'Recency':'最近1次消费时间间隔（R）是指用户最近一次消费距离现在多长时间了。'
                             '对于最近1次消费时间间隔（R），上一次消费离得越近，也就是R的值越小，用户价值越高。',
                   'Frequency':'消费频率（F）是指用户一段时间内消费了多少次。对于消费频率（F），购买频率越高，也就是F的值越大，用户价值越高。',
                   'Monetary':'消费金额（M）是指用户一段时间内的消费金额。对于消费金额（M），消费金额越高，也就是M的值越大，用户价值越高。'
                   }
    method_cases = {'RFM分析使用': ['（1）使用原始数据计算出R、F、M值；',
                                   '（2）给R、F、M值按价值打分，例如按价值从低到高分为1～5分；',
                                   '（3）计算价值的平均值，如果某个指标的得分比价值的平均值低，标记为低。如果某个指标的得分比价值的平均值高，标记为高；',
                                   '（4）和用户分类规则表比较，得出用户分类。']}
    return method_title, method_capt, method_cases


# 'AARRR模型分析方法' (AARRR Model Analysis Method)
def aarrr_analysis():
    method_title = 'AARRR模型分析方法'
    method_capt = 'AARRR模型涉及用户使用产品的整个流程，所以它可以帮助分析用户行为，为产品运营制定决策，从而实现用户增长。'
    method_cases = {'AARRR模型分析方法':
                    ['（1）获取用户（Acquisition）：用户如何找到我们？',
                     '（2）激活用户（Activation）：用户的首次体验如何？',
                     '（3）提高留存（Retention）：用户会回来吗？',
                     '（4）增加收入（Revenue）：如何赚到更多钱？',
                     '（5）推荐（Referral）：用户会告诉其他人吗？']}
    return method_title, method_capt, method_cases


# '漏斗分析方法' (Funnel Analysis Method)
def funnel_analysis():
    method_title = '漏斗分析方法'
    method_capt = ['漏斗分析方法衡量业务流程每一步的转化效率','漏斗分析的作用是定位问题节点，即找到出问题的业务环节在哪。',
                   '漏斗分析常用于用户转化分析或者用户流失分析，即用户转化率和用户流失率。']
    method_cases = {'举例': {'浏览量': 300, '点击量':100, '创建订单': 50, '支付':40}}
    return method_title, method_capt, method_cases



