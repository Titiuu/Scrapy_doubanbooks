import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class DoubanSpider(scrapy.Spider):
    name = 'douban'  # 爬虫名称
    baseurl = "https://book.douban.com"  # 基础url
    allowed_domains = ['book.douban.com']  # 爬取域名
    start_urls = ['https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4/']  # 小说预览页url
    books_number = 0  # 爬取书籍数量控制
    page_number = 0  # 爬取页面数量控制
    rules = [
        Rule(LinkExtractor(allow='https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4/[^/]+/?$')),
    ]  # 允许的链接爬取规则

    def parse(self, response):
        sel = scrapy.Selector(response)

        urls = sel.xpath(
            '//*[@id="subject_list"]//li[@class="subject-item"]//h2/a/@href').extract()
        for url in urls:
            print("crawl book link: ", url, ", id: ", url[32:-1])
            # url = https://book.douban.com/subject/3070863/
            subject_id = url[32:-1]
            # 先存在本地文件再逐步抓取书籍信息
            if self.books_number < 80:
                f = open('bookidlist.txt', 'a')

                f.write(subject_id + "\n")
                self.books_number += 1
        tagurl = sel.xpath(
            '//*[@id="subject_list"]/div[@class="paginator"]/span[@class="thispage"]/following-sibling::a[1]/@href').extract()
        if tagurl and self.page_number < 3:
            print("crawl booktag link: ", self.baseurl + tagurl[0])
            self.page_number += 1
            yield scrapy.Request(self.baseurl + tagurl[0], callback=self.parse)
