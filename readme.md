# Distributed Scraper

This is a distributed web crawler project built using **Scrapy-Redis** for distributed scheduling, **Celery** for managing proxy tasks, and **Redis Bloom Filter** for efficient duplicate filtering. 

## Features

- **Distributed Crawling:** Uses Scrapy-Redis to share the crawl queue across multiple nodes.
- **Duplicate Filtering:** Implements a custom deduplication filter using Redis Bloom Filter.
- **Proxy Management:** Integrates a proxy pool maintained with Celery tasks.
- **Fault Tolerance:** Supports persistent scheduling and proxy validation to remove non-functional proxies.

## Requirements

- Python 3.6+
- Redis
- [Scrapy](https://scrapy.org/)
- [scrapy-redis](https://github.com/rmax/scrapy-redis)
- [Celery](https://docs.celeryproject.org/)
- [redis-py](https://github.com/andymccurdy/redis-py)
- [RedisBloom](https://oss.redislabs.com/redisbloom/)

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```


# Project Configuration and Usage Notes

This document outlines the configuration and usage of various components in this project, including RedisBloom, Scrapy-Redis, a custom Bloom Filter, and a proxy pool managed by Celery.

---

## RedisBloom

- **Requirement:**  
  Ensure that your Redis server has the Bloom Filter module loaded.  
  Without RedisBloom, the Bloom filter commands (`BF.*`) will not be recognized.

- **How to Load:**  
  Start Redis with the RedisBloom module loaded:
  
  ```bash
  redis-server --loadmodule /path/to/redisbloom.so
  ```

---

## Scrapy-Redis

- **Configuration:**  
  In `settings.py`, Scrapy is configured to use `scrapy_redis.scheduler.Scheduler`.  
  This enables multiple Scrapy instances (across different machines) to share the same Redis queue.

---

## Custom Bloom Filter

- **Implementation:**  
  The `BloomDupeFilter` in `dupefilter.py` demonstrates how to initialize and use a Redis Bloom Filter to check if a URL has been seen.  
  Use this custom duplicate filter to prevent re-crawling URLs.

---

## Proxy Pool

- **Celery Tasks:**  
  The Celery tasks `fetch_proxies` and `validate_proxies` in `celery_app.py` provide a simple example of managing a pool of proxies stored in Redis.

- **Details:**
  - **`fetch_proxies`:** Customize this task to pull proxy lists from any source you prefer.
  - **`validate_proxies`:** Automatically removes non-responsive proxies from the pool.

---

## Example Spider

- **Usage:**  
  The example spider (`my_spider.py`) uses the `RedisSpider` class from `scrapy_redis`.  
  It reads the `redis_key` (in this case, `myspider:start_urls`) to obtain the start URLs.

- **Adding Start URLs:**  
  To populate the list with URLs, use the Redis CLI:
  
  ```bash
  redis-cli lpush myspider:start_urls "http://example.com" "http://example2.com"
  ```

  Each time you push new URLs to the `myspider:start_urls` list, the spider will pick them up (if it’s running) or on the next run.

---

## How to Use

### 1. Install Dependencies

Install the necessary dependencies using pip:

```bash
pip install -r requirements.txt
```

### 2. Run Redis

- **Ensure:**  
  Redis is running on your machine.  
  Update the connection URLs in the code if needed.

- **RedisBloom:**  
  Make sure RedisBloom is loaded as shown above.

### 3. Start the Crawler

Navigate to your scrapy project directory and start the crawler:

```bash
cd scrapy_project
scrapy crawl myspider
```

**Important:**  
Before (or during) the crawl, add start URLs to Redis:

```bash
redis-cli lpush myspider:start_urls "http://example.com"
```

You can also add URLs from within a script/program.

### 4. Start Celery Worker and Beat

In two separate terminals, run the following commands:

```bash
celery -A celery_app worker --loglevel=info
```

```bash
celery -A celery_app beat --loglevel=info
```

This starts the Celery worker processes that handle fetching and validating proxies (`fetch_proxies` and `validate_proxies`) at scheduled intervals.

---

By following these instructions, you can effectively manage your scraping infrastructure using RedisBloom, Scrapy-Redis, and a proxy pool with Celery.
```