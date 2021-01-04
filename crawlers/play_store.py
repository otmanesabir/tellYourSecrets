## SELENIUM
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from crawlers import selenium_util as su
from crawlers import crawler_interface as ci

## MISC.
from datetime import datetime
import time

## LOCAL
from models import review_details
from models import app_info
import logger as lg

log = lg.setup_custom_logger(__name__)

class play_store_crawler(ci.crawler_interface):
    def get_reviews(self, app: app_info.app_info):
        driver = su.create_chrome_driver()
        review_list = []
        new_date = None
        try:
            driver.get(app.android_link + "&showAllReviews=true")
            dropdown = driver.find_element_by_css_selector("div.MocG8c.UFSXYb.LMgvRb.KKjvXb")
            dropdown.click()
             # TODO stop making it rely on random sleep
            time.sleep(2)
            newest = driver.find_elements_by_css_selector("div.MocG8c.UFSXYb.LMgvRb")[3]
            newest.click()
             # TODO stop making it rely on random sleep
            time.sleep(2)
            reviews = driver.find_elements_by_css_selector("div[jscontroller='H6eOGe']")
            for review in reviews:
                if len(review_list) == self.MAX_REVIEWS:
                    log.info(f'Reached review limit: {self.MAX_REVIEWS}')
                    break
                r_desc = review.find_element_by_css_selector("div.UD7Dzf").text
                r_app_name = app.app_name
                temp_date = review.find_element_by_css_selector("span.p2TkOb").text
                r_date = datetime.strptime(temp_date, '%B %d, %Y').date()
                app.last_saved_review = r_date
                rating_wrapper = review.find_element_by_css_selector("span.nt2C1d")
                r_fullStars = len(rating_wrapper.find_elements_by_css_selector("div.vQHuPe.bUWb7c"))
                review_list.append(review_details.review_details(app.bundle_id, r_app_name, r_desc, r_date, r_fullStars))
                log.info(f'Added review {len(review_list)}/{self.MAX_REVIEWS}')
                if new_date is None:
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
            driver.get(f'https://play.google.com/store/search?q={name}&c=apps')
            # TODO switch to wait statement
            blocks = driver.find_elements_by_css_selector("div.ImZGtf.mpg5gc")
            i = 0
            for block in blocks:
                if (i < start_idx):
                    i += 1
                    continue
                if (len(app_list)) == self.APP_LIMIT:
                    log.info(f'Reached app limit: {self.APP_LIMIT}')
                    break
                name_link = block.find_element_by_css_selector("div.b8cIId.ReQCgd.Q9MA7b")
                r_appName = name_link.text
                r_android_link = name_link.find_element_by_tag_name("a").get_attribute("href")
                r_bundleID = r_android_link.split("id=")[1]
                app_list.append(app_info.app_info(r_bundleID, r_appName, r_android_link, None, None))
        except Exception as e:
            log.error("scraper failed\n" + str(e))
        finally:
            driver.quit()
        return app_list
    
