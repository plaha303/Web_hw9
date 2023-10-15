from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from hw9_spider.spiders.quotes import QuotesSpider
from hw9_spider.spiders.authors import AuthorsSpider


process = CrawlerProcess(get_project_settings())

process.crawl(QuotesSpider)
process.crawl(AuthorsSpider)
process.start()
