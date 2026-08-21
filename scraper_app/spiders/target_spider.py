import scrapy
from datetime import datetime, timezone
from scraper_app.items import ScrapedDataItem

class TargetSpider(scrapy.Spider):
    name = "target_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        """
        @url http://quotes.toscrape.com/
        @returns items 1 15
        @returns requests 0 2
        @scrapes item_id title url content scraped_at
        """
        for quote in response.css("div.quote"):
            item = ScrapedDataItem()
            
            content = quote.css("span.text::text").get() or ""
            author = quote.css("small.author::text").get() or ""
            author_url_ext = quote.css("span a::attr(href)").get()
            
            # Using content + author as a pseudo ID for deduplication
            item['item_id'] = f"{content[:20]}-{author}" 
            item['title'] = author
            item['url'] = response.urljoin(author_url_ext) if author_url_ext else response.url
            item['content'] = content
            item['scraped_at'] = datetime.now(timezone.utc).isoformat()
            
            yield item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse, errback=self.errback_httpbin)

    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))
        
        if failure.check(scrapy.exceptions.IgnoreRequest):
            self.logger.error("Ignored request")
