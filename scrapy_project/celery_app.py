from celery import Celery
import requests
import redis

app = Celery('tasks', broker='redis://localhost:6379/0')
redis_conn = redis.StrictRedis()
PROXY_KEY = 'proxy_pool'

@app.task
def fetch_proxies():
    proxies = ['http://1.2.3.4:8080', 'http://5.6.7.8:8080']
    for proxy in proxies:
        try:
            resp = requests.get('http://httpbin.org/ip', proxies={'http': proxy}, timeout=5)
            if resp.ok:
                redis_conn.zadd(PROXY_KEY, {proxy: resp.elapsed.microseconds})
        except:
            pass

@app.task
def validate_proxies():
    proxies = redis_conn.zrange(PROXY_KEY, 0, -1)
    for proxy in proxies:
        proxy = proxy.decode()
        try:
            resp = requests.get('http://httpbin.org/ip', proxies={'http': proxy}, timeout=5)
            if not resp.ok:
                redis_conn.zrem(PROXY_KEY, proxy)
        except:
            redis_conn.zrem(PROXY_KEY, proxy)