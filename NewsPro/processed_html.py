# -*- coding: utf-8 -*-
import re

def get_processed_html(bodyhtml):
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_iframe = re.compile('<\s*iframe[^>]*>[^<]*<\s*/\s*iframe\s*>')  # iframe
    re_ins = re.compile('<\s*ins[^>]*>[^<]*<\s*/\s*ins\s*>')  # ins
    re_div_redundant = re.compile('<\s*div[^>]*>[\s]*<\s*/\s*div\s*>')  # 多余的空div
    bodyhtml = re_ins.sub('', bodyhtml)  # 去点ins
    bodyhtml = re_script.sub('', bodyhtml)  # 去掉SCRIPT
    bodyhtml = re_style.sub('', bodyhtml)  # 去掉style
    bodyhtml = re_iframe.sub('', bodyhtml)  # 去掉iframe
    bodyhtml = re_div_redundant.sub('', bodyhtml)  # 去掉多余的空div

    label_list = ['div', 'strong', 'span', ]
    for label in label_list:
        re_labell = re.compile('<\s*' + label)  # 左标签
        re_labelr = re.compile('/\s*' + label + '\s*>')  # 右标签
        bodyhtml = re_labell.sub('<p', bodyhtml)  # 把左标签改为p标签的左标签
        bodyhtml = re_labelr.sub('/p>', bodyhtml)  # 把右标签改为p标签的右标签
    return bodyhtml
    # print(bodyhtml)
    # with open('./a.html','w',encoding='utf-8') as fp:
    #     fp.write(bodyhtml)