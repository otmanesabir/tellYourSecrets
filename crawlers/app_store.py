## SELENIUM
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from crawlers import selenium_util as su

# INTERNAL
from models import review_details
from models import app_info


import time
import logger as lg
from datetime import datetime
from urllib.request import urlopen


def search_app_name(name, start_idx):
    driver = su.create_chrome_driver() 
    wait = WebDriverWait(driver, 10)
    app_list = []
    try:
        driver.get(f'https://fnd.io/#/us/search?mediaType=ios&term={name}')
        # TODO change this to explicit wait
        time.sleep(5)
        main_list = driver.find_element_by_css_selector("ul.ii-list.media-list")
        list_items = main_list.find_elements_by_css_selector("li.ii-row.media")
        i = 0
        for item in list_items:
            if (i < start_idx):
                i += 1
                continue
            if (len(app_list)) == 10:
                lg.logger.info(f'Reached review limit: {i}')
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
            app_list.append(app_info.app_info(r_bundleID, r_appName, "", r_apple_link, None))
    except Exception as e:
        lg.logger.error("scraper failed: " + str(e))
    finally:
        driver.quit()
    return app_list

def get_reviews(app_details, reviewLimit):
    driver = su.create_chrome_driver() 
    wait = WebDriverWait(driver, 10)
    review_list = []
    try:
        driver.get(app_details.apple_link + "#see-all/reviews")
        time.sleep(3)
        lg.logger.info("launched webdriver")
        blocks = driver.find_elements_by_css_selector("div.ember-view.l-column--grid.l-column.small-12.medium-6.large-4.small-valign-top.l-column--equal-height")
        for block in blocks:
            if (len(review_list) == reviewLimit):
                lg.logger.info(f'Reached review limit: {reviewLimit}')
                break
            class_name = block.find_element_by_css_selector("span.we-star-rating-stars-outlines").find_element_by_tag_name("span").get_attribute("class")
            r_rating = int(class_name[-1])
            temp_date = block.find_element_by_css_selector("time.we-customer-review__date").text
            r_date = datetime.strptime(temp_date, "%m/%d/%Y").date()
            r_desc = block.find_element_by_css_selector("div.we-clamp.ember-view").text
            review_list.append(review_details.review_details(app_details.app_name, r_desc, r_date, r_rating))
            lg.logger.info(f'Added review {len(review_list)}/{reviewLimit}') 
    except Exception as e:
        lg.logger.error("scraper failed" + str(e))
    finally:
        driver.quit()
    return review_list 