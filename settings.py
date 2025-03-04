# 启用Redis调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True  # 支持断点续爬

# 使用自定义布隆过滤器去重
DUPEFILTER_CLASS = "myproject.dupefilter.BloomDupeFilter"

# Redis连接配置
REDIS_URL = 'redis://localhost:6379/0'

# 启用代理中间件
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.ProxyMiddleware': 543,
}
