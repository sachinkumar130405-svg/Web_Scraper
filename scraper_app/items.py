import scrapy

class ScrapedDataItem(scrapy.Item):
    # Unique identifier (e.g., ID or URL) used for deduplication
    item_id = scrapy.Field() 
    
    # Scraped data fields
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    
    # Metadata
    scraped_at = scrapy.Field() # Timestamp of extraction
