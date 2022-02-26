import scrapy


class SuperspiderSpider(scrapy.Spider):
    name = 'superspider'
    start_urls = ['http://x.com/']

    import scrapy


class ParisSpider(scrapy.Spider):
    name = 'paris'
    start_urls = ['https://www.remax.com/ny/bayside/home-details/32-22-204th-st-bayside-ny-11361/5360832612196598319']


    def parse_page(self, response):
            # loop over all cover link elements that link off to the large
            # cover of the magazine and yield a request to grab the cove
            # data and image
            for href in response.xpath("//a[contains(., 'Large Cover')]"):
                yield scrapy.Request(href.xpath("@href").extract_first(),
                    self.parse_covers)

            # extract the 'Next' link from the pagination, load it, and
            # parse it
            next = response.css("div.pages").xpath("a[contains(., 'Next')]")
            yield scrapy.Request(next.xpath("@href").extract_first(), self.parse_page)

    def parse(self, response):
        raw_image_urls = response.css('.image img ::attr(src)').getall()
        raw_href_imgs = response.css('span.title a::attr(href)').getall()
        raw_src_imgs = response.css('.product-list img::attr(src)').extract()
        clean_image_urls=[]
        for img_url in raw_image_urls:
            clean_image_urls.append(response.urljoin(img_url))
        xpath = self.parse_page(self, response)
        yield {
            'image_urls': clean_image_urls,
            'href_image_urls': raw_href_imgs,
            'src_image_urls': raw_href_imgs,
            'xpath: ': xpath
        }