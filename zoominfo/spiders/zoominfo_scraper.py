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
            'headquarters': response.xpath("//*[@class='vertical-gap first']/descendant::div/span/text()").getall(),
              'phone': response.xpath("//*[@class='vertical-gap']/descendant::span/text()").getall(),
            'revenue': response.xpath("//h3[text()='Revenue']/descendant::span/text()").getall(),
            'employees_num': response.xpath("//h3[text()='Employees']/following-sibling::div[1]/span/text()").getall(),
            'website': response.xpath("//*[@class='vertical-gap website-link']/descendant::a/text()").getall(),
            'industry': response.xpath("//*[@class='company-chips-wrapper']/descendant::div/a/text()").getall()
        }
#headquarters parent
#//*[@id="left-container"]/div[1]/app-company-overview/div/div/div/div[1]/app-icon-text[1]/div/div[2]
#headquarters text
#//*[@id="left-container"]/div[1]/app-company-overview/div/div/div/div[1]/app-icon-text[1]/div/div[2]/span
#phone number parent
#//*[@id="left-container"]/div[1]/app-company-overview/div/div/div/div[1]/app-icon-text[2]
#phone number text
#//*[@id="left-container"]/div[1]/app-company-overview/div/div/div/div[1]/app-icon-text[2]/div/div[2]/span
#website parent
#//*[@id="left-container"]/div[1]/app-company-overview/div/div/div/div[1]/app-icon-text[3]
#website text
#//*[@id="left-container"]/div[1]/app-company-overview/div/div/div/div[1]/app-icon-text[3]/div/a
#Revenue parent
#//*[@id="left-container"]/div[1]/app-company-overview/div/div/div/div[1]/app-icon-text[4]
#Revenue text
#//*[@id="left-container"]/div[1]/app-company-overview/div/div/div/div[1]/app-icon-text[4]/div/div[2]/span
#Industry Wrappers
#//*[@id="left-container"]/div[1]/app-company-overview/div/div/div/div[1]/div[1]
#Industry Text
#//*[@id="left-container"]/div[1]/app-company-overview/div/div/div/div[1]/div[1]/app-chips[1]/div/a
#//*[@id="left-container"]/div[1]/app-company-overview/div/div/div/div[1]/div[1]/app-chips[2]/div/a
#/*[@id="left-container"]/div[1]/app-company-overview/div/div/div/div[1]/div[1]/app-chips[3]/div/a
