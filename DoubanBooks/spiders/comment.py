import scrapy
import time
import jieba.analyse
import re


class CommentSpider(scrapy.Spider):
    name = 'comment'  # 爬虫名称
    allowed_domains = ['book.douban.com']  # 域名
    tfidf = {}  # 关键词字典
    data = open('bookidlist.txt').readlines()  # 书籍主页链接列表
    start_urls = ['https://book.douban.com/subject/' + data[0] + '/comments/']  # 开始的url
    booknum = 0  # 爬取60本书后结束

    def parse(self, response):
        time.sleep(2)  # 时延，避免爬取过快
        print("sleep a while")
        sel = scrapy.Selector(response)
        comid = response.url[32:-1]
        comid = re.search(r'\d+', str(comid)).group(0)
        com1 = sel.xpath(
            '/html/body/div[3]/div[1]/div/div[1]/div/div[4]/div[1]/ul/li[1]/div[2]/p/span/text()').extract()
        if com1:
            com1s = com1[0].strip()
        else:
            com1s = '无短评'
        print(com1s)
        com2 = sel.xpath(
            '/html/body/div[3]/div[1]/div/div[1]/div/div[4]/div[1]/ul/li[2]/div[2]/p/span/text()').extract()
        if com2:
            com2s = com2[0].strip()
        else:
            com2s = '无短评'
        print(com2s)
        com = com1s + com2s
        keywords = jieba.analyse.extract_tags(com, topK=10, withWeight=False, allowPOS=())
        self.tfidf[comid] = keywords
        self.booknum += 1
        if self.booknum == 60:
            print(self.tfidf)
            tilist = self.tfidf.items()
            for i in tilist:
                f = open('tfidf.txt', 'a')
                f.write(str(i[0]) + ': ' + str(i[1]) + '\n')
        if self.booknum < 60:
            yield scrapy.Request('https://book.douban.com/subject/' + self.data[self.booknum] + '/comments/', callback=self.parse)

