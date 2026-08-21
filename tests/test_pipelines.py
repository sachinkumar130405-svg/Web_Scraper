import unittest
from unittest.mock import patch, MagicMock
from scrapy.exceptions import DropItem
from scraper_app.pipelines import DuplicatesPipeline, MongoDBPipeline

class TestDuplicatesPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = DuplicatesPipeline()
        self.spider = MagicMock()

    def test_process_item_missing_id(self):
        item = {'title': 'Test Title'}
        with self.assertRaises(DropItem):
            self.pipeline.process_item(item, self.spider)

    def test_process_item_new_item(self):
        item = {'item_id': 'id123', 'title': 'Test Title'}
        processed_item = self.pipeline.process_item(item, self.spider)
        self.assertEqual(processed_item, item)
        self.assertIn('id123', self.pipeline.seen_ids)

    def test_process_item_duplicate(self):
        item1 = {'item_id': 'id123', 'title': 'Test Title 1'}
        item2 = {'item_id': 'id123', 'title': 'Test Title 2'}
        self.pipeline.process_item(item1, self.spider)
        
        with self.assertRaises(DropItem):
            self.pipeline.process_item(item2, self.spider)

class TestMongoDBPipeline(unittest.TestCase):
    @patch('scraper_app.pipelines.pymongo.MongoClient')
    def test_open_spider(self, mock_mongo_client):
        pipeline = MongoDBPipeline('mongodb://localhost:27017/', 'test_db')
        spider = MagicMock()
        
        mock_client_instance = MagicMock()
        mock_mongo_client.return_value = mock_client_instance
        
        pipeline.open_spider(spider)
        
        mock_mongo_client.assert_called_once_with('mongodb://localhost:27017/')
        self.assertEqual(pipeline.client, mock_client_instance)
        self.assertEqual(pipeline.db, mock_client_instance['test_db'])
        mock_client_instance['test_db']['scraped_data'].create_index.assert_called_once_with('item_id', unique=True)
        
    @patch('scraper_app.pipelines.pymongo.MongoClient')
    def test_process_item(self, mock_mongo_client):
        pipeline = MongoDBPipeline('mongodb://localhost:27017/', 'test_db')
        spider = MagicMock()
        pipeline.db = MagicMock()
        
        item = {'item_id': 'id123', 'title': 'Test Title'}
        
        processed_item = pipeline.process_item(item, spider)
        
        pipeline.db['scraped_data'].update_one.assert_called_once_with(
            {'item_id': 'id123'},
            {'$set': dict(item)},
            upsert=True
        )
        self.assertEqual(processed_item, item)
