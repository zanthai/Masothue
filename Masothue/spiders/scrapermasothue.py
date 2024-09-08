import scrapy
from Masothue.items import MasothueItem

class ScrapermasothueSpider(scrapy.Spider):
    name = "scrapermasothue"
    allowed_domains = ["masothue.com"]

    # cai nay la fake thiet bi tai bi ban ip 
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    def start_requests(self):
        yield scrapy.Request(url='https://masothue.com/tra-cuu-ma-so-thue-theo-tinh/', callback=self.parse_list)
    def parse_list(self, response):
        # Lay danh sach tata ca cac tinh
        province_links = response.xpath('//*[@id="main"]/section/div/table/tbody/tr/td/a/@href').getall()
        if province_links:
            first_province_link = province_links[0]
            remaining_provinces = province_links[1:]
            yield scrapy.Request(
                url=response.urljoin(first_province_link),
                callback=self.parse_province,
                meta={'remaining_provinces': remaining_provinces}
            )
    # Lấy danh sách các công ty trong tỉnh
    def parse_province(self, response): 
        company_links = response.xpath('//*[@id="main"]/section/div/div/div/h3/a/@href').getall()
        for company_link in company_links:
            item = MasothueItem()
            item['courseUrl'] = response.urljoin(company_link)
            request = scrapy.Request(
                url=response.urljoin(company_link),
                callback=self.parseCourseDetailPage,
                meta={'datacourse': item, 'remaining_provinces': response.meta.get('remaining_provinces')}
            )
            yield request
        if not company_links:  # Kiem tra neu khong co du lieu cong ty nao nua thi chuyen sang tinh khac
            yield from self.process_next_province(response)

    def parseCourseDetailPage(self, response):
        item = response.meta['datacourse']
        item['tencty'] = response.xpath('normalize-space(string(//*[@id="main"]/section[1]/div/table/thead/tr/th/span/text()))').get()
        item['tenqt'] = response.xpath('normalize-space(string(//*[@id="main"]/section[1]/div/table[1]/tbody/tr[1]/td[2]/span/text()))').get()
        item['masothue'] = response.xpath('normalize-space(string(//*[@id="main"]/section[1]/div/table[1]/tbody/tr[3]/td[2]/span/text()))').get()
        item['diachi'] = response.xpath('normalize-space(string(//*[@id="main"]/section[1]/div/table[1]/tbody/tr[4]/td[2]/span/text()))').get()
        item['nguoidaidien'] = response.xpath('normalize-space(string(//*[@id="main"]/section[1]/div/table[1]/tbody/tr[5]/td[2]/span/a/text()))').get()
        item['phone'] = response.xpath('normalize-space(string(//*[@id="main"]/section[1]/div/table[1]/tbody/tr[6]/td[2]/span/text()))').get()
        item['ngayhoatdong'] = response.xpath('normalize-space(string(//*[@id="main"]/section[1]/div/table[1]/tbody/tr[7]/td[2]/span/text()))').get()
        item['quanly'] = response.xpath('normalize-space(string(//*[@id="main"]/section[1]/div/table[1]/tbody/tr[8]/td[2]/span/text()))').get()
        item['loaihinh'] = response.xpath('normalize-space(string(//*[@id="main"]/section[1]/div/table[1]/tbody/tr[9]/td[2]/a/text()))').get()
        item['tinhtrang'] = response.xpath('normalize-space(string(//*[@id="main"]/section[1]/div/table[1]/tbody/tr[10]/td[2]/a/text()))').get()
        yield item

        # Neu la cty cuoi cung trong danh sach thi chu7yen sang tinh tiep theo
        if response.meta.get('remaining_provinces'):
            yield from self.process_next_province(response)

     # Chuyen sang tinh tiep theo neu da xu ly xong tinh hientai
    def process_next_province(self, response):
        remaining_provinces = response.meta.get('remaining_provinces', [])
        if remaining_provinces:
            next_province_link = remaining_provinces[0]
            remaining_provinces = remaining_provinces[1:]
            yield scrapy.Request(
                url=response.urljoin(next_province_link),
                callback=self.parse_province,
                meta={'remaining_provinces': remaining_provinces}
            )
