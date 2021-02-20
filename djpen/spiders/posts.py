import scrapy

class PostsSpider(scrapy.Spider):
    name = 'posts'
    allowed_domains = ['djpen.kemendag.go.id']
    start_urls = ['http://djpen.kemendag.go.id/app_frontend/imp_profiles/view/1']


    def parse(self, response):
        page_number = 1
        while page_number<15002:
            self.link = f'http://djpen.kemendag.go.id/app_frontend/imp_profiles/view/{page_number}'
            page_number += 1
            yield scrapy.Request(url = self.link, callback = self.parse_item)


    def parse_item(self, response):
        title = response.css("#body > div > div.left.grid_9 > h1 ::text").get()
        address = ''.join(response.css("#body > div > div.left.grid_9 > div.article > div > p:nth-child(1) ::text").getall())
        address = address.replace(" ","")
        address = address.replace("\t","")
        address = address.replace("\n","")
        detail = response.css(".detail")
        full_desc = ''.join(response.css(".detail ::text").getall())
        full_desc = full_desc.replace(" ","")
        full_desc = full_desc.replace("\t","")
        full_desc = full_desc.replace("\n","")
        data = {}
        if title:
            data['page'] = self.link[-1]
            data['title'] = title
            data['address'] = address
            data['phone'] = detail.xpath("p[2]/text()").get()
            data['fax'] = detail.xpath("p[3]/text()").get()
            data['email'] = detail.xpath("p[4]/text()").get()
            data['website'] = detail.xpath("p[5]/text()").get()
            data['contact'] = response.css("#body > div > div.left.grid_9 > div.article > div > ul:nth-child(7) > li ::text").getall()
            data['products'] = response.css("#body > div > div.left.grid_9 > div.article > div > ul:nth-child(9) > li ::text").getall()
            data['full_desc'] = full_desc
        else:
            data.remove()
        yield data