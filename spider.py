#coding=utf=-8
from bs4 import BeautifulSoup #网页解析，获取数据
import re     #正则表达式，进行文字匹配
import urllib.request,urllib.error    #指定URL，获取网页数据
import xlwt    #进行excel操作
import sqlite3   #进行SQLite数据库操作

def main():
    savepath="豆瓣电影top250.xls"
    baseurl="https://movie.douban.com/top250?start="
    #1爬取网页
    datalist=getData(baseurl)
    #askURL("https://movie.douban.com/top250?start=0")
    #保存数据
    saveData(datalist,savepath)




findlink=re.compile(r'<a href="(.*?)">')    #创建正则表达式对象，表示规则（字符串模式）
findImagSrc=re.compile(r'<img alt=".*src="(.*?)"',re.S)   #re.S忽略换行符
findTitle=re.compile(r'<span class="title">(.*?)</span>')
findRating=re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
findJudge=re.compile(r'<span>(\d*?)人评价</span>')
findInq=re.compile(r'<span class="inq"(.*?)</span>')
findBd=re.compile(r'<p class="">(.*?)</p>',re.S)
#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):       #调用获取页面信息10次
        url=baseurl+str(i*25)    
        html=askURL(url)       #保存获取到的网页源码
        

        #逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):   #查找符合要求的字符串，形成列表
            #print(item)
            data = []  #保存一部电影的所有信息
            item = str(item)

            link = re.findall(findlink,item)[0]   #re库通过正则表达式来查找
            data.append(link)

            ImgSrc = re.findall(findImagSrc,item)[0]
            data.append(ImgSrc)

            titles=re.findall(findTitle,item)
            if len(titles)>2:
                ctitle=titles[0]
                data.append(ctitle)
                otitle=titles[1].replace("/","")
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(" ")   #外文名留空

            rating=re.findall(findRating,item)
            data.append(rating)

            judgeNum=re.findall(findJudge,item)[0]
            data.append(judgeNum)

            inq=re.findall(findInq,item)
            if len(inq)!=0:
                inq=inq[0].replace("。","")
                data.append(inq)
            else:
                data.append(" ")

            bd=re.findall(findBd,item)[0]
            bd=re.sub(r'<br(\s+)?/>(\s+)?'," ",bd)   #去掉<br/>
            bd=re.sub('/'," ",bd)   #替换、
            data.append(bd.strip())


            datalist.append(data)   #将一部电影的信息加入datalist
    return datalist

#得到一个网页的内容
def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    req=urllib.request.Request(headers=head,url=url)
    html=""
    try:
        response=urllib.request.urlopen(req)
        html=response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html


def saveData(datalist,savepath):
    workbook = xlwt.Workbook(encoding="utf-8")  # 创建Workbook对象
    worksheet = workbook.add_sheet('豆瓣电影250',cell_overwrite_ok=True)  # cell_overwrite_ok=True  可以覆盖单元格
    col=("电影详情链接","图片链接","影片中文名","影片英文名","评分","评价数","概括","相关信息")
    for i in range(0,8):
        worksheet.write(0,i,col[i])
    for i in range(0,250):
        print("第%d条"%(i+1))
        data=datalist[i]
        for j in range(0,8):
            worksheet.write(i+1,j,data[j])
    workbook.save(savepath)  # 保存数据表


if __name__ == "__main__":
    main()
