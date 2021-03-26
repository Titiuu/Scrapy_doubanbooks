import scrapy
import time
import jieba.analyse
import re


class CommentSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = ['book.douban.com']
    tfidf = {}
    data = open('bookidlist.txt').readlines()
    start_urls = ['https://book.douban.com/subject/' + data[0] + '/comments/']
    booknum = 0

    def parse(self, response):
        time.sleep(2)
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

