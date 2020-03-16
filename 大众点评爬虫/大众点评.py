import requests
from lxml import etree
import json


class dzdp():
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Host': 'www.dianping.com', 'Upgrade-Insecure-Requests': '1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive'}
        self.Cookie = {'_lxsdk_cuid': '16d32508714c8-04cb990264c00f-5373e62-144000-16d32508714c8',
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
                       '_lxsdk_s': '16f143a64bc-76d-841-9c2%7C%7C317'}

        self.url_pages = [
            'http://www.dianping.com/search/keyword/5/10_新街口/p{}'.format(i) for i in range(1, 51)]
        self.session = requests.session()
        self.f = open('大众点评.json', 'a+', encoding='utf-8')

    def save(self, html_text, html_num):
        # 餐馆名
        name_list = html_text.xpath(
            '//*[@id="shop-all-list"]/ul/li/div[2]/div[1]/a[1]/h4/text()')
        # 星级
        star_list = html_text.xpath(
            '//*[@id="shop-all-list"]/ul/li/div[2]/div[2]/span/@class')
        # 评价数
        people_list = []
        for i in range(1, 16):
            temp_text = html_num.xpath(
                '//*[@id="shop-all-list"]/ul/li[{}]/div[2]/div[2]/a[1]/b/text()'.format(i))
            temp_num = html_num.xpath(
                '//*[@id="shop-all-list"]/ul/li[{}]/div[2]/div[2]/a[1]/b/svgmtsi/text()'.format(i))
            for i in range(len(temp_num)):
                temp_num[i] = temp_num[i].replace('\uf4ea', '2')
                temp_num[i] = temp_num[i].replace('\ue686', '3')
                temp_num[i] = temp_num[i].replace('\uf4b8', '4')
                temp_num[i] = temp_num[i].replace('\uf459', '5')
                temp_num[i] = temp_num[i].replace('\uf691', '6')
                temp_num[i] = temp_num[i].replace('\ue617', '7')
                temp_num[i] = temp_num[i].replace('\uecb1', '8')
                temp_num[i] = temp_num[i].replace('\ue6a7', '9')
                temp_num[i] = temp_num[i].replace('\ue9cd', '0')
            if (len(temp_text) > 1):
                temp = ''.join(temp_text[:1] + temp_num)
            else:
                temp = ''.join(temp_text[:1] + temp_num + temp_text[1:])
            people_list.append(temp)

        # 人均花费
        cost_list = []
        for i in range(1, 16):
            temp_text = html_num.xpath(
                '//*[@id="shop-all-list"]/ul/li[{}]/div[2]/div[2]/a[2]/b/text()'.format(i))
            temp_num = html_num.xpath(
                '//*[@id="shop-all-list"]/ul/li[{}]/div[2]/div[2]/a[2]/b/svgmtsi/text()'.format(i))
            for i in range(len(temp_num)):
                temp_num[i] = temp_num[i].replace('\uf4ea', '2')
                temp_num[i] = temp_num[i].replace('\ue686', '3')
                temp_num[i] = temp_num[i].replace('\uf4b8', '4')
                temp_num[i] = temp_num[i].replace('\uf459', '5')
                temp_num[i] = temp_num[i].replace('\uf691', '6')
                temp_num[i] = temp_num[i].replace('\ue617', '7')
                temp_num[i] = temp_num[i].replace('\uecb1', '8')
                temp_num[i] = temp_num[i].replace('\uf4ea', '9')
                temp_num[i] = temp_num[i].replace('\ue9cd', '0')
            cost_list.append(''.join(temp_text + temp_num))
        # 推荐菜
        cook_list = []
        for i in range(1, 16):
            temp = html_text.xpath(
                '//*[@id="shop-all-list"]/ul/li[{}]/div[2]/div[4]/a/text()'.format(i))
            cook_list.append(','.join(temp))

        for i in range(15):
            item = {}
            item['餐馆'] = name_list[i]
            item['星级'] = star_list[i][-2:]
            item['评价数'] = people_list[i]
            item['人均'] = cost_list[i]
            item['推荐菜'] = cook_list[i]
            #item['网友推荐菜'] = html.xpath() if len(item['网友推荐菜']) > 0 else None
            if ((item['星级'] == '50') | (item['星级'] == '45') | (item['星级'] == '40')):
                self.f.write(json.dumps(item, ensure_ascii=False, indent=2))
            self.f.write('\n')

    def run(self):
        for url_page in self.url_pages:
            response = self.session.get(
                url_page, headers=self.headers, cookies=self.Cookie)
            html_text = etree.HTML(response.text)
            html_num = etree.HTML(response.content)
            # url_list = html.xpath(
            #     '//*[@id="shop-all-list"]/ul/li/div[1]/a/@href')
            # for url in url_list:
            #     print(url)
            #     # 获取响应
            #     responce = self.get_response(url)
            #     print(response.status_code)
            #     # 抓取数据并保存
            #     return response.text
            #     html = etree.HTML(response.text)
            #     self.save(html)
            self.save(html_text, html_num)
            print(url_page)
        self.f.close()


test = dzdp()
test.run()
