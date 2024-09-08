# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import json
import csv
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class JsonDBMasothuePipeline:
    def process_item(self, item, spider):
        with open('jsondatamasothue.json', 'a', encoding='utf-8') as file:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            file.write(line)
        return item
    
class CSVDBMasothuePipeline:
    def open_spider(self, spider):
        self.file = open('csvdatamasothue.csv', 'w', encoding='utf-8', newline='')
        self.writer = csv.writer(self.file, delimiter=',')
        self.writer.writerow([
            'Ten Cong Ty', 'Ten Quan Tri', 'Ma So Thue', 'Dia Chi', 
            'Nguoi Dai Dien', 'Phone', 'Ngay Hoat Dong', 'Quan Ly', 
            'Loai Hinh', 'Tinh Trang'
        ])
    
    def close_spider(self, spider):
        self.file.close()
    
    def process_item(self, item, spider):
        self.writer.writerow([
            item.get('tencty', ''),
            item.get('tenqt', ''),
            item.get('masothue', ''),
            item.get('diachi', ''),
            item.get('nguoidaidien', ''),
            item.get('phone', ''),
            item.get('ngayhoatdong', ''),
            item.get('quanly', ''),
            item.get('loaihinh', ''),
            item.get('tinhtrang', '')
        ])
        return item