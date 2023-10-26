# -*-coding:utf-8 -*-

"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：python 3.9
# Description： 易经
"""
import json
import os
import random

file_path = os.path.abspath(__file__)
file_path = os.path.dirname(file_path)
with open(os.path.join(file_path, 'yi.json'), 'r') as f:
    yi_json = json.load(f)

gua8_data = yi_json['八卦']
gua64_data = yi_json['六十四卦']

gua8_code_name = {gua8_data[i]['八卦编号']: i for i in gua8_data}
gua64_code_name = {i['卦象号']: i['卦名简体'] for i in gua64_data.values()}


def phrase():
    phrase1 = '乾三连 坤六断 震仰盂 艮覆碗 离中虚 坎中满 兑上缺 巽下断'
    phrase2 = '上下经卦名次序歌:' \
              '乾坤屯蒙需讼师， 比小畜兮履泰否。同人大有谦豫随， 蛊临观兮噬嗑贲。剥复无妄大畜颐， 大过坎离三十备。' \
              '咸恒遁兮及大壮， 晋与明夷家人睽。蹇解损益夬姤萃， 升困井革鼎震继。艮渐归妹丰旅巽， 兑涣节兮中孚至。' \
              '小过既济兼未济， 是为下经三十四。'
    phrase3 = '上下经卦变歌:' \
              '讼自遁变泰归妹，否从渐来随三位。首困噬嗑未济兼，蛊三变贲井既济。噬嗑六五本益生，贲原于损既济会。'\
              '无妄讼来大畜需，咸旅恒丰皆疑似。晋从观更睽有三，离与中孚家人系。蹇利西南小过来，解升二卦相为赘。' \
              '鼎由巽变渐涣旅，涣自渐来终于是。'
    phrase_list = [phrase1, phrase2, phrase3]
    return phrase_list


# 获得六十四卦 本卦，上下卦，综卦，错卦，交互卦，卦象
def gua_profile(gua64='乾'):
    profile = {}
    gua64_code = gua64_data[gua64]['卦象号']
    shang_gua = gua8_code_name[gua64_code[0:3]]
    xia_gua = gua8_code_name[gua64_code[3:6]]
    zong_gua = gua64_code_name[gua64_code[3:6]+gua64_code[0:3]]
    cuo_gua_code = ''.join([['1', '0'][int(i)] for i in gua64_code])
    cuo_gua = gua64_code_name[cuo_gua_code]
    jiaohu_gua = gua64_code_name[gua64_code[2:5]+gua64_code[1:4]]
    yang = '▅▅▅▅▅'
    yin = '▅▅　▅▅'
    gua_img = ''.join([[f'{yin}\n\n', f'{yang}\n\n'][int(i)] for i in gua64_code])
    yao_name = ['上爻', '五爻', '四爻', '三爻', '二爻', '初爻']
    for i, j in enumerate(yao_name):
        profile[j] = [yin, yang][int(gua64_code[i])]
    profile.update({'本卦': gua64, '上卦': shang_gua, '下卦': xia_gua, '综卦': zong_gua,
                    '错卦': cuo_gua, '交互卦': jiaohu_gua, '卦象': gua_img})
    return profile


# 获得卦的各爻属性
def yao_info(gua64='乾'):
    gua64_code = gua64_data[gua64]['卦象号']
    yao_dict = dict()
    pos = ['上', '五', '四', '三', '二', '初']
    for i, j in enumerate(gua64_code):
        num = '九' if j == '1' else '六'
        yao_name = pos[i]+num if i in [0, 5] else num+pos[i]
        yao_intro = ''
        yao_intro += '得正、当位；' if (i % 2, j) in [(1, '1'), (0, '0')] else '失正、不当位；'
        if (i, j) in [(1, '1'), (4, '0')]:
            yao_intro += '中正；'
        elif (i, j) in [(1, '0'), (4, '1')]:
            yao_intro += '得中；'
        if j == '0' and (i < 5) and gua64_code[i+1] == '1':
            yao_intro += '乘刚；'
        if j == '0' and (i > 0) and gua64_code[i-1] == '1':
            yao_intro += '承阳；'
        if i < 3 and int(j)+int(gua64_code[i+3]) == 1:
            yao_intro += '有应；'
        elif i >= 3 and int(j)+int(gua64_code[i-3]) == 1:
            yao_intro += '有应；'
        else:
            yao_intro += '无应；'
        yao_dict.update({yao_name: yao_intro})
    return yao_dict


yao_value = {'老阴': {'爻值': '0', '变爻': '1', '变爻象': '1'},
             '少阳': {'爻值': '1', '变爻': '0', '变爻象': '1'},
             '少阴': {'爻值': '0', '变爻': '0', '变爻象': '0'},
             '老阳': {'爻值': '1', '变爻': '1', '变爻象': '0'}}
bian_yao = {'0': '无变爻，本卦卦辞为占',
            '1': '一变爻，之卦动爻爻辞为占',
            '2': '二变爻，同阴同阳，之卦上位动爻爻辞为占；一阴一阳，之卦阴爻动爻爻辞为占',
            '3': '三变爻，之卦居中动爻爻辞为占',
            '4': '四变爻，之卦居下静爻爻辞为占',
            '5': '五变爻，之卦静爻爻辞为占',
            '6': '六变爻，本卦是乾坤，本卦用爻爻辞为占；本卦是其他卦，之卦卦辞为占'}


# 随机起爻
def random_qi_yao():
    yin_yang = ['0', '1']
    yao_code = [random.choice(yin_yang) for _ in range(3)]
    num = yao_code.count('1')
    yao_value_list = ['老阴', '少阳', '少阴', '老阳']
    yao_attr = yao_value_list[num]
    return yao_attr


# 随机起卦
def random_qi_gua():
    r_qi_gua = {'本卦卦象': '', '本卦变爻': '', '变卦卦象': ''}
    for _ in range(6):
        yao_attr = random_qi_yao()
        yao_v_a = yao_value[yao_attr]
        r_qi_gua['本卦卦象'] = yao_v_a['爻值']+r_qi_gua['本卦卦象']
        r_qi_gua['本卦变爻'] = yao_v_a['变爻']+r_qi_gua['本卦变爻']
        r_qi_gua['变卦卦象'] = yao_v_a['变爻象']+r_qi_gua['变卦卦象']
    return r_qi_gua


# yao_attr_list = [yao6, yao5, yao4, yao3, yao2, yao1]
# 输入卦
def make_qi_gua(yao_attr_list):
    m_qi_gua = {'本卦卦象': '', '本卦变爻': '', '变卦卦象': ''}
    for i in yao_attr_list:
        yao_v_a = yao_value[i]
        m_qi_gua['本卦卦象'] += yao_v_a['爻值']
        m_qi_gua['本卦变爻'] += yao_v_a['变爻']
        m_qi_gua['变卦卦象'] += yao_v_a['变爻象']
    return m_qi_gua


# 解卦
def zhan_gua(qi_gua):
    ben_gua = qi_gua['本卦卦象']
    zhi_gua = qi_gua['变卦卦象']
    bian_yao_li = qi_gua['本卦变爻']
    num = list(bian_yao_li).count('1')
    zhan_gua_intro = bian_yao[str(num)]
    ben_gua64_name = gua64_code_name[ben_gua]
    bian_gua64_name = gua64_code_name[zhi_gua]
    yao_name = ['上爻', '五爻', '四爻', '三爻', '二爻', '初爻']
    expl = ''
    if num == 0:
        expl = gua64_data[ben_gua64_name]['卦辞']
    elif num == 1:
        pos = bian_yao_li.find('1')
        yao_pos = yao_name[pos]
        expl = gua64_data[bian_gua64_name][yao_pos+'爻辞']
    elif num == 2:
        pos0 = bian_yao_li.find('1', 0)
        pos1 = bian_yao_li.find('1', pos0+1)
        if ben_gua[pos0] == ben_gua[pos1]:
            yao_pos = yao_name[pos0]
            expl = gua64_data[bian_gua64_name][yao_pos+'爻辞']
        else:
            if zhi_gua[pos0] == '0':
                yao_pos = yao_name[pos0]
                expl = gua64_data[bian_gua64_name][yao_pos+'爻辞']
            else:
                yao_pos = yao_name[pos1]
                expl = gua64_data[bian_gua64_name][yao_pos+'爻辞']
    elif num == 3:
        pos0 = bian_yao_li.find('1', 0)
        pos1 = bian_yao_li.find('1', pos0+1)
        yao_pos = yao_name[pos1]
        expl = gua64_data[bian_gua64_name][yao_pos+'爻辞']
    elif num == 4:
        pos0 = bian_yao_li.find('0', 0)
        pos1 = bian_yao_li.find('0', pos0+1)
        yao_pos = yao_name[pos1]
        expl = gua64_data[bian_gua64_name][yao_pos+'爻辞']
    elif num == 5:
        pos = bian_yao_li.find('0')
        yao_pos = yao_name[pos]
        expl = gua64_data[bian_gua64_name][yao_pos+'爻辞']
    elif num == 6:
        if ben_gua == '111111' or ben_gua == '000000':
            expl = gua64_data[ben_gua64_name]['用爻爻辞']
        else:
            expl = gua64_data[bian_gua64_name]['卦辞']
    return zhan_gua_intro, expl




# 周易精读笔记
# path = '/Users/xx/Desktop/周易精读笔记.docx'
#doc = docx.Document(path)
#    for para in doc.paragraphs[:2]:
#        print(para.text)

