# -*- coding: utf-8 -*-

# Scrapy settings for douban_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'douban_crawler'

SPIDER_MODULES = ['douban_crawler.spiders']
NEWSPIDER_MODULE = 'douban_crawler.spiders'

COOKIES_ENABLED = False  #禁止COOKIES
DOWNLOAD_TIMEOUT = 15
DOWNLOAD_DELAY = 2

# Enables scheduling storing requests queue in redis.
SCHEDULER = "douban_crawler.scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True

# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "douban_crawler.scrapy_redis.dupefilter.RFPDupeFilter"

SCHEDULER_QUEUE_CLASS = 'douban_crawler.scrapy_redis.queue.SpiderPriorityQueue'

REDIS_HOST = 'localhost'

REDIS_PORT = 6379

REDIE_URL = None

#MONGO_DB
MONGO_URI = 'mongodb://127.0.0.1:27017'
MONGO_DATABASE = 'douban_crawler'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'douban_crawler.middlewares.RotateUserAgentMiddleware': 543,
#    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110
}


# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'douban_crawler.pipelines.MongoPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,

}

RETRY_HTTP_CODES = [403, 404, 400]
#COMMANDS_MODULE = 'HouseInfoSpider.commands'

# 去重队列的信息
FILTER_URL = None
FILTER_HOST = 'localhost'
FILTER_PORT = 6379
FILTER_DB = 0
