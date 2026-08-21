import pymongo
from scrapy.exceptions import DropItem

class DuplicatesPipeline:
    def __init__(self):
        self.seen_ids = set()

    def process_item(self, item, spider):
        item_id = item.get('item_id')
        if not item_id:
            raise DropItem("Missing item_id")
            
        if item_id in self.seen_ids:
            raise DropItem(f"Duplicate item found: {item_id}")
        else:
            self.seen_ids.add(item_id)
            return item

class MongoDBPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI', 'mongodb://localhost:27017/'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'scraper_db')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # Ensure index on item_id for deduplication in DB
        self.db['scraped_data'].create_index('item_id', unique=True)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # Insert or update based on item_id
        self.db['scraped_data'].update_one(
            {'item_id': item['item_id']},
            {'$set': dict(item)},
            upsert=True
        )
        return item
