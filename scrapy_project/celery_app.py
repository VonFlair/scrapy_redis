from celery import Celery
import requests
import redis

# Initialize the Celery app with Redis as the broker
app = Celery('tasks', broker='redis://localhost:6379/0')

# Establish a connection to Redis
redis_conn = redis.StrictRedis()
PROXY_KEY = 'proxy_pool'

@app.task
def fetch_proxies():
    """
    Fetch proxies from a free proxy website (this is a sample implementation).
    Valid proxies are added to a sorted set with their response time as the score.
    """
    # Example proxy list (replace with dynamic fetching logic)
    proxies = ['http://1.2.3.4:8080', 'http://5.6.7.8:8080']
    for proxy in proxies:
        try:
            resp = requests.get('http://httpbin.org/ip', proxies={'http': proxy}, timeout=5)
            if resp.ok:
                # Add the proxy with response time (microseconds) as score
                redis_conn.zadd(PROXY_KEY, {proxy: resp.elapsed.microseconds})
        except Exception:
            pass

@app.task
def validate_proxies():
    """
    Validate proxies stored in the proxy pool.
    Remove proxies that fail the validation check.
    """
    proxies = redis_conn.zrange(PROXY_KEY, 0, -1)
    for proxy in proxies:
        proxy = proxy.decode()
        try:
            resp = requests.get('http://httpbin.org/ip', proxies={'http': proxy}, timeout=5)
            if not resp.ok:
                redis_conn.zrem(PROXY_KEY, proxy)
        except Exception:
            redis_conn.zrem(PROXY_KEY, proxy)
