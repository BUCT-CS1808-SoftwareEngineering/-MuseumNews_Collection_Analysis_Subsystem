from snownlp import SnowNLP
from cnsenti import Sentiment,Emotion
from bixin import predict
import bixin

def snow_res(text):
    s = SnowNLP(text)
    print(s.sentiments)
    if s.sentiments < 0.4:
        # 消极
        return -1
    elif s.sentiments > 0.6:
        # 中性
        return 0
    else:
        # 积极
        return 1

def cnsent_res(text):
    senti = Sentiment()
    res1 = senti.sentiment_count(text)
    print(res1)
    emo = Emotion()
    res2 = emo.emotion_count(text)
    print(res2)

def bixin_res(text):
    return predict(text)

text = ["乡村有约共话博物馆助力乡村振兴",
        "上海电影博物馆启动“光影初心 红色征途”主题活动",
        "[新闻眼]小伙复原黄金面具 三星堆博物馆:来上班!",
        "成都耗资12亿,迎来大型博物馆,占地85.3亩,将于2022年6月开放",
        "他家藏9道圣旨,借给博物馆展览后却意外丢了2道,赔了多少钱?",
        "当年被母亲宠坏,偷走湖南博物馆文物将其烧掉的少年,近况如何",
        "收藏非裔美国人头骨受质疑,这些博物馆准备怎么办?",
        "女间谍遭枪决,因长得太美,死后头颅做了防腐,至今被博物馆收藏",
        "中国文物报社将联合多家博物馆推出全国革命文物图片选萃展",
        "湖南省博物馆被盗走惊世文物，盗贼才17岁，死刑只能缓两年执行",
        "旅游时发现博物馆看管不严 西咸新区两男子夜盗文物——“比开拉土车还挣钱”",
        "欲与同事发生性关系遭拒，他痛下杀手，昨日被执行死刑"]

#
# for i in text:
#     print(i)
#     # snow_res(i)
#     res = predict(i)
#     # print(bixin.cut(i))
#     # print(predict(i))
#     print(res)
#     # cnsent_res(i)
# title = ""
# print(predict(title))
