# Scrapy settings for scrapy_project
# This file contains settings for integrating Scrapy-Redis, custom duplicate filtering, and proxy middleware.

BOT_NAME = 'scrapy_project'

SPIDER_MODULES = ['scrapy_project.spiders']
NEWSPIDER_MODULE = 'scrapy_project.spiders'

# Enable the Redis-based scheduler to share the request queue across crawlers
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True  # Persist the crawl queue between runs

# Use the custom Bloom Filter-based duplicate filter
DUPEFILTER_CLASS = "scrapy_project.dupefilter.BloomDupeFilter"

# Redis connection settings
REDIS_URL = 'redis://localhost:6379/0'

# Enable the proxy middleware for requests
DOWNLOADER_MIDDLEWARES = {
    'scrapy_project.middlewares.ProxyMiddleware': 543,
}

# Other common settings
ROBOTSTXT_OBEY = True
