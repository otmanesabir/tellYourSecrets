## SELENIUM
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from crawlers import selenium_util as su
from crawlers import crawler_interface as ci

# INTERNAL
from models import review_details
from models import app_info


import time
import logger as lg
from datetime import datetime
from urllib.request import urlopen
from urllib.error import HTTPError

log = lg.setup_custom_logger(__name__)

class app_store_crawler(ci.crawler_interface):

    def get_reviews(self, app: app_info.app_info):
        driver = su.create_chrome_driver() 
        review_list = []
        new_date = None
        try:
            driver.get(app.apple_link + "#see-all/reviews")
            time.sleep(3)
            log.info("launched webdriver")
            blocks = driver.find_elements_by_css_selector("div.ember-view.l-column--grid.l-column.small-12.medium-6.large-4.small-valign-top.l-column--equal-height")
            for block in blocks:
                if (len(review_list) == self.MAX_REVIEWS):
                    log.info(f'Reached review limit: {self.MAX_REVIEWS}')
                    break
                class_name = block.find_element_by_css_selector("span.we-star-rating-stars-outlines").find_element_by_tag_name("span").get_attribute("class")
                r_rating = int(class_name[-1])
                temp_date = block.find_element_by_css_selector("time.we-customer-review__date").text
                r_date = datetime.strptime(temp_date, "%m/%d/%Y").date()
                r_desc = block.find_element_by_css_selector("div.we-clamp.ember-view").text
                review_list.append(review_details.review_details(app.bundle_id, app.app_name, r_desc, r_date, r_rating))
                log.info(f'Added review {len(review_list)}/{self.MAX_REVIEWS}')
                if (new_date is None):
                    new_date = r_date
            if (app.update_date(new_date)):
                log.info(f"Updated last review date to: {new_date}")
            else:
                log.warning(f"Failed to update the last review date.")
        except Exception as e:
            log.error("scraper failed\n" + str(e))
        finally:
            driver.quit()
        return review_list 

    def search_app_name(self, name: str, start_idx: int):
        driver = su.create_chrome_driver() 
        app_list = []
        try:
            driver.get(f'https://fnd.io/#/us/search?mediaType=ios&term={name}')
            # TODO change this to explicit wait
            time.sleep(5)
            main_list = driver.find_element_by_css_selector("ul.ii-list.media-list")
            list_items = main_list.find_elements_by_css_selector("li.ii-row.media")
            i = 0
            for item in list_items:
                try:
                    if (i < start_idx):
                        i += 1
                        continue
                    if (len(app_list)) == self.APP_LIMIT:
                        log.info(f'App Store crawler reached app limit: {i}')
                        break
                    r_appName = item.find_element_by_css_selector("div.ember-view.ii-name").text
                    r_apple_link = item.find_element_by_css_selector("a.btn.btn-itunes.btn-itunes-buy").get_attribute("href")

                    # steps to find the bundle ID:
                        # first get id from the link
                        # then use it in the link we previosuly found
                        # download the file
                        # convert to JSON and find bundle_ID

                    app_id = r_apple_link.split("id")[1].split("?")[0]
                    data = str(urlopen(f'https://itunes.apple.com/lookup?id={app_id}').read(), 'utf-8')
                    r_bundleID = data.split('bundleId":"')[1].split('"')[0]
                    app_list.append(app_info.app_info(r_bundleID, r_appName, None, r_apple_link, None))
                except HTTPError as httpE:
                    # skip this line and continue
                    log.error(f"App Store crawler failed to get BundleID for {r_appName}")
                    pass
                except Exception as e:
                    log.error(f"App Store crawler failed.")
        except Exception as e:
            log.error("scraper failed: " + str(e))
        finally:
            driver.quit()
        return app_list