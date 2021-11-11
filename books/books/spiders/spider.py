from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy


class SpiderSpider(CrawlSpider):
    name = 'spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    base_url = 'http://books.toscrape.com/'

    rules = [Rule(LinkExtractor(allow='catalogue'),
                  callback='parse_filter', follow=True)]

    def parse_filter(self, response):
        exists = response.xpath('//div[@id="product_gallery"]').extract_first()
        if exists:
            title = response.xpath('//div/h1/text()').extract_first()

            relative_image = response.xpath(
                '//div[@class="item active"]/img/@src').extract_first().replace('../..', '')
            final_image = self.base_url + relative_image

            price = response.xpath(
                '//div[contains(@class, "product_main")]/p[@class="price_color"]/text()').extract_first()
            stock = response.xpath(
                '//div[contains(@class, "product_main")]/p[contains(@class, "instock")]/text()').extract()[1].strip()
            stars = response.xpath(
                '//div/p[contains(@class, "star-rating")]/@class').extract_first().replace('star-rating ', '')
            description = response.xpath(
                '//div[@id="product_description"]/following-sibling::p/text()').extract_first()
            upc = response.xpath(
                '//table[@class="table table-striped"]/tr[1]/td/text()').extract_first()
            price_excl_tax = response.xpath(
                '//table[@class="table table-striped"]/tr[3]/td/text()').extract_first()
            price_inc_tax = response.xpath(
                '//table[@class="table table-striped"]/tr[4]/td/text()').extract_first()
            tax = response.xpath(
                '//table[@class="table table-striped"]/tr[5]/td/text()').extract_first()
            number_of_reviews = response.xpath(
                '//table[@class="table table-striped"]/tr[5]/td/text()').extract_first().replace('\u00a3', '')

            yield {
                'Title': title,
                'Image': final_image,
                'Price': price,
                'Stock': stock,
                'Stars': stars,
                'Description': description,
                'Upc': upc,
                'Price after tax': price_excl_tax,
                'Price incl tax': price_inc_tax,
                'Tax': tax,
                'Number of reviews': number_of_reviews,
            }
        else:
            print(response.url)