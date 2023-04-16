import scrapy


class ZoominfoSpider(scrapy.Spider):
    name = 'zoominfo'

    def start_requests(self):
        with open("input.csv", 'r') as input_file:
            for company_name in input_file:
                company = company_name.strip()
                url = f"https://www.google.com.ua/search?q={company + '+zoominfo+overview'}"
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
            'headquarters': response.xpath("//h3[text()='Headquarters']/following-sibling::div/span/text()").get(),
            'phone': response.xpath("//h3[text()='Phone Number']/following-sibling::div/span/text()").get(),
            'revenue': response.xpath("//h3[text()='Revenue']/following-sibling::div/span/text()").get(),
            'employees_num': response.xpath("//h3[text()='Revenue']/following-sibling::div/span/text()").get(),
            'website': response.xpath("//h3[text()='Website']/following-sibling::div/span/text()div/a/text()").get(),
            'industry': response.xpath("//*[@id="left-container"]/div[1]/app-company-overview/div/div/div/div[1]/div[1]/following-sibling::a/text()").get()
        }
