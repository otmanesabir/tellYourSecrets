## SELENIUM
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from crawlers import selenium_util as su

from models import review_details
from datetime import datetime

import time
import logger as lg

def getReviews(app_details, reviewLimit):
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
                print(f'Reached review limit: {reviewLimit}')
                break
            class_name = block.find_element_by_css_selector("span.we-star-rating-stars-outlines").find_element_by_tag_name("span").get_attribute("class")
            r_rating = int(class_name[-1])
            temp_date = block.find_element_by_css_selector("time.we-customer-review__date").text
            r_date = datetime.strptime(temp_date, "%m/%d/%Y").date()
            r_desc = block.find_element_by_css_selector("div.we-clamp.ember-view").text
            review_list.append(review_details.review_details(app_details.app_name, r_desc, r_date, r_rating))
            print(f'Added review {len(review_list)}/{reviewLimit}') 
    except Exception as e:
        lg.logger.error("scraper failed" + str(e))
    finally:
        driver.quit()
    return review_list 