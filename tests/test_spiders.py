import unittest
from scrapy.http import HtmlResponse, Request
from scraper_app.spiders.target_spider import TargetSpider

class TestTargetSpider(unittest.TestCase):
    def setUp(self):
        self.spider = TargetSpider()

    def test_parse(self):
        html_content = b"""
        <html>
            <body>
                <div class="quote">
                    <span class="text">"The world as we have created it is a process of our thinking."</span>
                    <span>by <small class="author">Albert Einstein</small>
                    <a href="/author/Albert-Einstein">(about)</a>
                    </span>
                </div>
                <li class="next"><a href="/page/2/">Next</a></li>
            </body>
        </html>
        """
        request = Request(url='http://quotes.toscrape.com/')
        response = HtmlResponse(url='http://quotes.toscrape.com/', request=request, body=html_content)
        
        results = list(self.spider.parse(response))
        
        # Should yield 1 item and 1 request
        self.assertEqual(len(results), 2)
        
        item = results[0]
        self.assertEqual(item['title'], 'Albert Einstein')
        self.assertEqual(item['content'], '"The world as we have created it is a process of our thinking."')
        self.assertIn('item_id', item)
        self.assertIn('scraped_at', item)
        self.assertEqual(item['url'], 'http://quotes.toscrape.com/author/Albert-Einstein')
        
        req = results[1]
        self.assertIsInstance(req, Request)
        self.assertEqual(req.url, 'http://quotes.toscrape.com/page/2/')
