from bs4 import BeautifulSoup
import urllib.request
import time
# 获取网页
def get_page(url):
    headers = {'User-Agent':'Mozilla/5.0'}
    Request = urllib.request.Request(url, headers=headers)

    while True:
        try:
            response = urllib.request.urlopen(Request, timeout=3)
            html = response.read()
            return html
        except Exception as e:
            print(e)
            print('重连中...')
            time.sleep(3)


# 解析网页
def parser_page(url):
    html = get_page(url)
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    # 获取文章标题
    title = soup.select('.bookname  h1')[0].get_text()
    # 获取文章内容
    text = soup.select('#content')[0]
    # 处理文章内容
    sentences = str(text.get_text()).split()
    theContent = ''
    for one in sentences:
        theContent = theContent + '  ' + one + '\n'
    return (title, theContent)

if __name__ == '__main__':
    # 填写下载地址
    aim_url = 'https://www.biduo.cc/biquge/34_34140/'

    html = get_page(aim_url)
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    urlList = soup.select('#list dl dd a')
    bookname = soup.select('#info h1')[0].get_text()
    for i,each in enumerate(urlList):
        # 若是断开了，修改这里的百分比小数，重启程序继续爬取
        # if i/len(urlList) <= 0.9999:
        #     print(i/len(urlList))
        #     continue
        eachHref = each.get('href')
        # 小说名字
        f = open(bookname+'.txt','a+',encoding = 'utf-8')
        (title,content) = parser_page('https://www.biduo.cc/' + eachHref)
        tmp = title + '\n' + content
        f.write(tmp)
        print('共' + str(len(urlList)) + '章，目前下载第' + str(i) + '章。当前进度为{:.2%}'.format(i / len(urlList)))
        time.sleep(1)


print('共' + str(len(urlList)) + '章，目前下载第' + str(len(urlList)) + '章。当前进度为100.00%')
print('下载完成！')

f.close()
