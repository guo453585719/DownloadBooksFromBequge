from bs4 import BeautifulSoup
import urllib.request
import time
# 获取网页
def get_page(url):
    headers = {'User-Agent':'Mozilla/5.0', 'Cookie':'__guid=129273610.1462615317714271700.1581307330628.9175; Hm_lvt_01cfde1abb745824aa94af8908e8fb2c=1581307332; jieqiVisitTime=jieqiArticlesearchTime%3D1581307335; jieqiVisitId=article_articleviews%3D474; __gads=ID=4f065f80a1a667f5:T=1581310527:S=ALNI_Mad3MiEsJT8xDmDTaMmcK_A8SVMYA; monitor_count=5; Hm_lpvt_01cfde1abb745824aa94af8908e8fb2c=1581310547'}
    Request = urllib.request.Request(url, headers=headers)

    #请求失败后，最多尝试10次连接
    maxTryNum = 10
    for tries in range(maxTryNum):
        try:
            response = urllib.request.urlopen(Request)
            html = response.read()
            return html
        except:
            print('请求网页失败,重试' + str(tries) + '次')
            if tries < (maxTryNum - 1):
                continue
            else:
                print("something wrong!")
                break



# 解析网页
def parser_page(url):
    html = get_page(url)
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    # 获取文章标题
    title = soup.select('.bookname  h1')[0].get_text()
    # 获取文章内容
    text = soup.select('#content')[0]
    # 处理文章内容
    newstr = '------------\n' + title + '\n'
    sentences = str(text.get_text()).split()
    theContent = ''
    for one in sentences:
        theContent = theContent + '  ' + newstr + '\n'
    return (title, theContent)

if __name__ == '__main__':
    aim_url = 'https://www.biduo.cc/biquge/1_1476/'
    html = get_page(aim_url)
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    urlList = soup.select('#list dl dd a')
    for i,each in enumerate(urlList):
        # 若是断开了，修改这里的百分比小数，重启程序继续爬取
        # if i/len(urlList) < 0.4334:
        #     print(i/len(urlList))
        #     continue
        eachHref = each.get('href').replace('/biquge/1_1476/', '')
        # 小说名字
        f = open('神话版三国.txt','a+',encoding = 'utf-8')
        (title,content) = parser_page(aim_url + eachHref)
        tmp = title + '\n' + content
        f.write(tmp)
        print('downloading...{:.2%}'.format(i/len(urlList)))
        time.sleep(1)


    f.close()
