import requests  
from bs4 import BeautifulSoup 
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


customer_header = {
    "referer":"https://news.naver.com/main/read.naver",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

"""
https://search.naver.com/search.naver?
where=news&sm=tab_pge&query=%EB%B0%B1%EC%8B%A0&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=37&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=41
"""

"""
1 - 1    (page-1)*10 + 1   (1-1)*10+1 = 1
2 - 11   (2-1)*10 +1        11
3 - 21   (3-1)*10 +1        21  
4 - 31   (4-1)*10 +1        31
5 - 41   (5-1)*10+1        = 41
""" 
def getList(keyword, page_cnt, filename):

    file = open(filename, "w", encoding="utf8")
    page=1 
    for page in range(1, page_cnt+1):
        url="https://search.naver.com/search.naver?where=news&sm=tab_pge&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=28&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all"
        url=url+"&query=" + keyword 
        url=url+"&start=" + str((page-1)*10 + 1) 
        response = requests.get(url, headers=customer_header) 
        if response.status_code==200: 
            contents = response.content
            soup = BeautifulSoup(contents, 'html.parser') 
            alinkList = soup.find_all("a",class_="sub_txt") 
            news = getDetail(alinkList)
            print(news)
            for line in news:
                file.write(line)

    #for문 종료하고나서 
    file.close()      


def getDetail(alinkList):
    news=[]
    for link in alinkList:
        #print(link['href'])
        if "https://news.naver.com/main" in link['href']:
            response = requests.get(link['href'], headers=customer_header) 
            if response.status_code==200:
                soup = BeautifulSoup(response.content, 'html.parser')
                #print(response.content )
                title = soup.find("h3", id="articleTitle")
                news.append(title.text)
                #print(title.text)
                contents = soup.find("div", id="articleBodyContents")
                news.append(contents.text)
                #print(contents.text)
    return news


def createWordCloud(filename,keyword):
    dir=path.dirname(__file__) #현재 디렉토리 가져온다
    f = open(filename, 'r',encoding='utf-8')
    text=f.read()

    filename = path.join(dir, "./data/코로나2.jpg")
    image = Image.open(filename) #이미지를 읽어서 
    alice_mask = np.array(image)

    image_colors=ImageColorGenerator(alice_mask)
    stopwords=set(STOPWORDS)
    stopwords.add("있다")
    stopwords.add("위한")
    stopwords.add("함수")
    stopwords.add("오류를")
    stopwords.add("추가")
    stopwords.add("flash")
    stopwords.add("등")
    stopwords.add("function")
    stopwords.add("고")
    stopwords.add("말했다")
    stopwords.add("_flash_removeCallback")
    stopwords.add("기자")
    stopwords.add("이라고")
    stopwords.add("읽었다")
    stopwords.add("예정이다")
    stopwords.add("등이")
    stopwords.add("우회하기")
    stopwords.add("며")
    stopwords.add("밝혔다")

    wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask,stopwords=stopwords,font_path='C:/Windows/Fonts/BMHANNAAir_ttf_0.TTF' )
    wc.generate(text)
    wc.recolor(color_func=image_colors)

    wc.to_file(path.join(dir, "{}.png".format(keyword))) #결과 저장
    plt.imshow(wc, interpolation='bilinear') #화면출력
    plt.show()


if __name__=="__main__":
    keyword=input("검색어 : ")
    page_cnt=int(input("page : "))
    filename=input("파일이름.txt : ")
    getList(keyword,page_cnt,filename)
    createWordCloud(filename,keyword)
