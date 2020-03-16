from selenium import webdriver
from lxml import etree
import json


class dzdp():
    def __init__(self):
        self.Cookie = {'navCtgScroll': '0',
                       '_lxsdk_cuid': '16d32508714c8-04cb990264c00f-5373e62-144000-16d32508714c8',
                       '_lxsdk': '16d32508714c8-04cb990264c00f-5373e62-144000-16d32508714c8',
                       '_hc.v': 'dc12c917-706f-6193-6ac0-14e39a38ef9c.1568507203',
                       'cy': '5',
                       'cye': 'nanjing',
                       's_ViewType': '10',
                       '_lx_utm': 'utm_source%3Dgoogle%26utm_medium%3Dorganic',
                       'cityid': '5',
                       'default_ab': 'index%3AA%3A3',
                       'switchcityflashtoast': '1',
                       'm_flash2': '1',
                       'seouser_ab': 'index%3AA%3A1%7CshopList%3AA%3A1',
                       'dper': 'ad7b5e2e5c58c75fbb8665376e75e8e2c13570dab677605609deecb2c3c9b0d599b7de4817cfd3443a632a7e2687811bdd3701da36e304c26da369a4bec07be35e7b25d6c37367fdb1ac3d328526114687a47c9a811c074ae4ef12581158dfce',
                       'ua': 'dpuser_9145061873',
                       'ctu': 'ea85409e3ee56b3293fd76446f84b1bc08dbbf0b7e9fdbfaf95b3a18ecf0a7e4',
                       'uamo': '13913114957',
                       'll': '7fd06e815b796be3df069dec7836c3df',
                       '_lxsdk_s': '16f143a64bc-76d-841-9c2%7C%7C87'}
        self.url_pages = [
            'http://www.dianping.com/search/keyword/5/10_新街口/p{}'.format(i) for i in range(2, 5)]
        self.driver = webdriver.Chrome()
        self.f = open('大众点评.josn', 'w+')

    def save(self):
        item = {}
        item['餐馆'] = self.driver.find_elements_by_xpath(
            '//*[@id="basic-info"]/h1/text()')
        item['星级'] = self.driver.find_elements_by_xpath(
            '//*[@id="basic-info"]/html[1]/span[1]/@class')[0][-2:] if len(self.driver.find_elements_by_xpath(
                '//*[@id="basic-info"]/html[1]/span[1]/@class')[0][-2:]) > 0 else None
        temp_text = self.driver.find_elements_by_xpath(
            '//*[@id="reviewCount"]/text()') if len(self.driver.find_elements_by_xpath(
                '//*[@id="reviewCount"]/text()')) > 0 else None
        temp_num = self.driver.find_elements_by_xpath(
            '//*[@id="reviewCount"]/d/text()')[:1] if len(self.driver.find_elements_by_xpath(
                '//*[@id="reviewCount"]/d')) > 0 else None
        item['评价数'] = ''.join(temp_text + temp_num)
        temp_text = self.driver.find_elements_by_xpath(
            '//*[@id="avgPriceTitle"]/text()') if len(self.driver.find_elements_by_xpath(
                '//*[@id="avgPriceTitle"]/text()')) > 0 else None
        temp_num = self.driver.find_elements_by_xpath(
            '//*[@id="avgPriceTitle"]/d/text()')[:1] if len(self.driver.find_elements_by_xpath(
                '//*[@id="avgPriceTitle"]/d')) > 0 else None
        item['人均'] = ''.join(temp_text + temp_num)
        #item['网友推荐菜'] = html.xpath() if len(item['网友推荐菜']) > 0 else None
        self.f.write(json.dumps(item))

    def num_decode(self, num_encoding):
        if (num_encoding == '&#xf09b'):
            return '4'
        if (num_encoding == '>&#xe4f1'):
            return '6'
        if (num_encoding == '&#xeed6'):
            return '8'

    def run(self):
        self.driver.get('http://www.dianping.com/search/keyword/5/10_新街口/p1')
        for url_page in self.url_pages:
            # 获取url
            url_list = self.driver.find_elements_by_xpath(
                '//*[@id="shop-all-list"]/ul/li/div[1]/a').get_attribute('href')
            for url in url_list:
                # 获取响应
                self.driver.get(url)
                self.save()
            print(url_page)
        self.f.close()


test = dzdp()
test.run()
