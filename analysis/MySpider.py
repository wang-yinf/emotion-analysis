import requests
import re
import paddlehub as hub
import urllib.parse
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')
from wordcloud import WordCloud
import jieba

average_score_positive = 0.0
average_score_negative = 0.0
probability_interval = [0.0, 0.0, 0.0, 0.0, 0.0]
i = 0
y = []
z = []


def Get_Comment(url):  # 抓取评论文本
    all = []
    '''
    cookie = 'll="108289";'\
             'bid=-DlbvH8p8iA;'\
             '_pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1589714960%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DQVc-gum-JzotO6Ss17A1nEm4wb8rDfRyoyNMnhSMRjEABAXQ0i-3gX5z8RCdoQhU%26wd%3D%26eqid%3Ded936bea00052d3e000000025ec1208b%22%5D;'\
             '_pk_ses.100001.8cb4=*;'\
             '__utma=30149280.765470221.1589714962.1589714962.1589714962.1;'\
             '__utmc=30149280;__utmz=30149280.1589714962.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic;'\
             'ap_v=0,6.0;'\
             '__gads=ID=fe736317bc884c6e:T=1589715484:S=ALNI_MaeIJ4HF5KN6-C6uuvMSsdNFfQW1Q;push_noty_num=0;'\
             'push_doumail_num=0;'\
             '__utmv=30149280.21469;'\
             '_pk_id.100001.8cb4=d097d8dad1e764b6.1589714960.1.1589715411.1589714960.;'\
             '__utmb=30149280.5.10.1589714962;'\
             'dbcl2="214695887:fPDk2InPTjI"'

    def coo_regular(cookie):
        coo = {}
        for k_v in cookie.split(';'):
            k, v = k_v.split('=', 1)
            coo[k.strip()] = v.replace('"', '')
        return coo

    cookies = coo_regular(cookie)
   '''
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    result = requests.get(url, headers=header)
    result.encoding = 'utf-8'
    compile = re.compile(r'<span class="short">(.*?)</span>')  # 使用正则表达式
    all.extend(compile.findall(result.text))
    return all


def Save_Comment(all):  # 保存评论文本
    n = '\n'
    i = 1
    with open('Comment.txt', 'w', encoding='utf-8') as f:
        for item in all:
            f.write("%d." % i)
            i = i + 1
            f.write(item)
            f.write(n)


def Analyse(name):  # 分析评论文本
    global i
    i = 0
    global probability_interval
    probability_interval = [0.0, 0.0, 0.0, 0.0, 0.0]
    probability_number = [0, 0, 0, 0, 0]
    global average_score_positive
    global average_score_negative
    sum_score_positive = 0.0
    sum_score_negative = 0.0

    with open(name, 'r', encoding='utf-8') as f1:  # 打开要处理的文件
        with open("Analyse.txt", 'w', encoding='utf-8') as f2:  # 打开处理后要存入的文件
            sentence = f1.readlines()
            senta = hub.Module(name='senta_lstm')
            results = senta.sentiment_classify(data={"text": sentence})

            for result in results:
                f2.write(result['text'])
                f2.write("此评论积极的可能性为")
                f2.write(str(result['positive_probs']))
                f2.write(" 消极的可能性为")
                f2.write(str(result['negative_probs']))
                f2.write("\n")
                sum_score_positive += result['positive_probs']
                sum_score_negative += result['negative_probs']
                global y
                y.insert(i, result['positive_probs'])
                # global z
                # z.insert(i,len(result['text']))

                i += 1
                if result['positive_probs'] < 0.2:
                    probability_number[0] = probability_number[0] + 1
                elif result['positive_probs'] < 0.4 and result['positive_probs'] >= 0.2:
                    probability_number[1] = probability_number[1] + 1
                elif result['positive_probs'] < 0.6 and result['positive_probs'] >= 0.4:
                    probability_number[2] = probability_number[2] + 1
                elif result['positive_probs'] < 0.8 and result['positive_probs'] >= 0.6:
                    probability_number[3] = probability_number[3] + 1
                elif result['positive_probs'] <= 1.0 and result['positive_probs'] >= 0.8:
                    probability_number[4] = probability_number[4] + 1
            for j in range(5):
                probability_interval[j] = float(probability_number[j] / i)

            average_score_positive = sum_score_positive / i
            average_score_negative = sum_score_negative / i


def Select(name):
    name1 = urllib.parse.quote(name)
    url = "https://movie.douban.com/j/subject_suggest?q=%s" % name1
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

    html = requests.get(url, headers=header)
    html = html.content.decode()

    compile = re.compile(r'"id":"(.*?)"}')  # 使用正则表达式匹配出id
    return compile.findall(html)[0]

def Select_book(name):
    name1 = urllib.parse.quote(name)
    url = "https://book.douban.com/j/subject_suggest?q=%s" % name1
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

    html = requests.get(url, headers=header)
    html = html.content.decode()

    compile = re.compile(r'"id":"(.*?)"}')  # 使用正则表达式匹配出id
    return compile.findall(html)[0]

def show_polarity():
    global average_score_positive
    global average_score_negative
    font = {'family': 'MicroSoft YaHei', 'weight': 'bold'}
    matplotlib.rc("font", **font)
    labels = 'positive', 'negative'
    sizes = [average_score_positive, average_score_negative]
    explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("电影的总体情感极性")
    plt.savefig("./pie_chart.png")
    plt.show()


def show_scatter():
    plt.figure(figsize=(10, 6), dpi=80)
    font = {'family': 'MicroSoft YaHei', 'weight': 'bold'}
    matplotlib.rc("font", **font)
    global i
    x = range(1, i + 1)
    global y
    plt.scatter(x, y)
    plt.grid()

    plt.savefig("./scatter.png")
    plt.title("电影短评的情感分析散点图")

    plt.show()


def show_bar_chart():
    plt.figure(figsize=(10, 6), dpi=80)
    font = {'family': 'MicroSoft YaHei', 'weight': 'bold'}
    matplotlib.rc("font", **font)
    global probability_interval
    b = ["0%~20%\n(1星)", "20%~40%\n(2星)", "40%~60%\n(3星)", "60%~80%\n(4星)", "80%~100%\n(5星)"]
    plt.bar(range(1, 6), probability_interval, width=0.5)

    plt.xlabel("积极的概率")
    plt.ylabel("占总论评论的百分比")

    plt.xticks(range(1, 6), b)
    plt.title("电影的预测评分百分比")
    plt.savefig("./bar_chart.png")

    plt.show()


def show_wordcloud():
    plt.figure(figsize=(15, 9), dpi=200)
    with open('Comment.txt', 'r', encoding='UTF-8') as f:
        text = f.read()
        text = " ".join(jieba.cut(text))
    wordcloud = WordCloud(font_path="C:\\Windows\\Fonts\\STXINGKA.TTF", background_color="white", width=1000,
                          height=500).generate(text)
    wordcloud.to_file('wordcloud.png')
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()


'''
def relation():
    plt.figure(figsize=(10, 6), dpi=80)
    font = {'family': 'MicroSoft YaHei', 'weight': 'bold'}
    matplotlib.rc("font", **font)
    global z
    global y

    plt.scatter(z, y)

    plt.savefig("./rela.png")
    plt.title("短评极性与相关性")
    plt.show()
'''


def main():
    name = input("请输入电影名：")
    id = Select(name)
    all = Get_Comment("https://movie.douban.com/subject/%s/comments?start=0&limit=20&sort=new_score&status=P" % id)
    Save_Comment(all)
    Analyse("Comment.txt")
    show_polarity()
    show_scatter()
    show_bar_chart()
    show_wordcloud()
    # relation()


if __name__ == '__main__':
    main()
