import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from selenium.webdriver.common.keys import Keys
from linkedin.spiders.search import extract_contact_info
from linkedin.spiders.selenium import SeleniumSpiderMixin, get_by_xpath_or_none

"""
Variable holding where to search for first profiles to scrape.
"""
NETWORK_URL = 'https://www.linkedin.com/mynetwork/invite-connect/connections/'


class UserSpider(SeleniumSpiderMixin, CrawlSpider):
    name = "users"
    count = 0
    max_count = 1
    is_visited = set()

    def wait_page_completion(self, driver):
        """
        Abstract function, used to customize how the specific spider have to wait for page completion.
        Blank by default
        :param driver:
        :return:
        """
        # waiting links to other users are shown so the crawl can continue
        get_by_xpath_or_none(driver, "//*/div[@class='pv-deferred-area ember-view']", wait_timeout=3)

    def start_requests(self):
        url = 'https://www.linkedin.com/in/yuyafukuchi261a861b1/'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        if self.count > self.max_count:
            return
        driver = response.meta.pop('driver')

        self.logger.info(f"Scrapy parse - get the names list. count: {self.count}")
        try:
            names = driver.find_elements_by_xpath('//div[@class="pv-browsemap-section"]/ul/li/a')
        except Exception as e:
            self.logger.error(e)
            return
        #names = driver.find_elements_by_xpath('//ul[@class="browsemap"]/li/a')
        frontier = []
        for name in names:
            link = name.get_attribute('href')
            profile_id = link.split('/')[-2]
            # すでに訪問したことあるprofileをはずす
            if profile_id in self.is_visited:
                continue
            self.is_visited.add(profile_id)

            item = extract_contact_info(self.api_client, profile_id)
            if not item:
                continue

            frontier.append(scrapy.Request(link, callback=self.parse))
            # itemを保存
            yield item

        driver.close()

        # 新たにリクエスト
        for f in frontier:
            self.count += 1
            if self.count > self.max_count:
                return
            yield f


