# Scrapy Web Scraper with MongoDB Integration

This project is a resilient web scraper built with Scrapy that extracts data and persists it in a local MongoDB database.

## Setup

1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
3. Install dependencies: `pip install -r requirements.txt`

## Running the Scraper

```bash
scrapy crawl target_spider
```

## Running Tests

```bash
pytest tests/
```
