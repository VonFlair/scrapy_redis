import random
import redis

class ProxyMiddleware:
    """
    Downloader middleware that assigns a random proxy from the Redis proxy pool.
    If a proxy causes an exception, it is removed from the pool.
    """
    def __init__(self):
        self.redis = redis.StrictRedis()
        self.proxy_key = 'proxy_pool'

    def process_request(self, request, spider):
        # Retrieve all proxies from the pool and set a random one for the request
        proxies = self.redis.zrange(self.proxy_key, 0, -1)
        if proxies:
            request.meta['proxy'] = random.choice(proxies).decode()

    def process_exception(self, request, exception, spider):
        # Remove the problematic proxy from the pool on exception
        if 'proxy' in request.meta:
            self.redis.zrem(self.proxy_key, request.meta['proxy'])
