import redis
from scrapy.utils.request import request_fingerprint

class BloomDupeFilter:
    """
    Custom duplicate filter that uses a Redis Bloom Filter.
    The Bloom Filter is initialized with a capacity of 1,000,000 elements and an error rate of 0.1%.
    """
    def __init__(self, server, key):
        self.server = server
        self.key = "bloom_filter"
        # Initialize the Bloom filter if it does not already exist
        if not self.server.execute_command('BF.EXISTS', self.key, 'init'):
            self.server.execute_command('BF.RESERVE', self.key, 0.001, 1000000)

    def request_seen(self, request):
        # Generate a fingerprint for the request and add it to the Bloom Filter
        fp = request_fingerprint(request)
        return bool(self.server.execute_command('BF.ADD', self.key, fp))
