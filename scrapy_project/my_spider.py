from scrapy_redis.spiders import RedisSpider

class MySpider(RedisSpider):
    """
    Example spider that reads URLs from the Redis list and processes responses.
    The 'redis_key' is used to populate the start URLs.
    """
    name = 'myspider'
    redis_key = 'myspider:start_urls'

    def parse(self, response):
        # Process the response and extract data
        yield {'url': response.url}
