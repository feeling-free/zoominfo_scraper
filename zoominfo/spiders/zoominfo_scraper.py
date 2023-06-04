import scrapy

class ZoominfoSpider(scrapy.Spider):
    name = 'zoominfo'
    def start_requests(self):
        with open("input.csv", 'r') as input_file:
            for company_name in input_file:
                company = company_name.strip()
                url = f"https://www.google.com/search?q={company + '+zoominfo+overview'}"
                req = scrapy.Request(url=url, callback=self.parse_google_results, cb_kwargs={"company": company})
                req.meta['proxy'] = None
                yield req

    def parse_google_results(self, response, **kwargs):
        all_links = response.css("a::attr(href)").getall()
        zoomlinks = [link for link in all_links if "www.zoominfo.com/c/" in link]
        yield scrapy.Request(url=zoomlinks[0], callback=self.parse, cb_kwargs=kwargs)

    def parse(self, response, **kwargs):
        yield {     
            'company': kwargs['company'],
            'headquarters': response.xpath("//*[@class='vertical-gap first']/descendant::div/span/text()").getall(),
              'phone': response.xpath("//*[@class='vertical-gap']/descendant::span/text()").getall(),
            'revenue': response.xpath("//*[@class='vertical-gap']/descendant::span/text()").getall(),
            'employees_num': response.xpath("//h3[text()='Employees']/following-sibling::div[1]/span/text()").getall(),
            'website': response.xpath("//*[@class='vertical-gap website-link']/descendant::a/text()").getall(),
            'industry': response.xpath("//div[@class='company-chips-wrapper']/descendant-or-self::div/a/text()").getall()
        }
