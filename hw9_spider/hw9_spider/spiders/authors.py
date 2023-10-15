import scrapy


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "json/authors.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        for author in response.css("div.quote"):
            author_info = {
                "fullname": author.css("small.author::text").get(),
            }
            author_about = response.urljoin(author.css("a::attr(href)").get())
            yield scrapy.Request(author_about, callback=self.parse_author_info, meta={"author_info": author_info})

            next_link = response.xpath("//li[@class='next']/a/@href").get()
            if next_link:
                yield scrapy.Request(url=self.start_urls[0] + next_link, callback=self.parse)

    def parse_author_info(self, response):
        author_info = response.meta["author_info"]
        author_info.update({
            "born_date": response.css("span.author-born-date::text").get(),
            "Born_location": response.css("span.author-born-location::text").get(),
            "description": response.css("div.author-description::text").get().strip(),
        })
        yield author_info
