## SELENIUM
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


## MISC.
import datetime as dt
import time

## LOCAL
import sim_utils as lg
import app_info
class review_details:
    def __init__(self, app_name, description, date, rating):
        self.app_name = app_name
        self.description = description
        self.date = date
        self.rating = rating

    def __repr__(self):
        return(
            f'ReviewDetails(\
                app_name={self.app_name}, \
                description={self.description}, \
                date={self.date}, \
                rating={self.rating}\
            )'
        )

def getReviews(app_details, reviewLimit):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get(app_details.android_link + "&showAllReviews=true")
        lg.logger.warning("launched webdriver")
        assert "Among Us" in driver.title
         ## Switch to newest view first
        dropdown = driver.find_element_by_css_selector("div.MocG8c.UFSXYb.LMgvRb.KKjvXb")
        dropdown.click()
         # TODO stop making it rely on random sleep
        time.sleep(3)
        newest = driver.find_elements_by_css_selector("div.MocG8c.UFSXYb.LMgvRb")[3]
        newest.click()
         # TODO stop making it rely on random sleep
        time.sleep(3)
        reviews = driver.find_elements_by_css_selector("div.UD7Dzf")
        for review in reviews:
            print(review.text)

    except NoSuchElementException as e:
        lg.logger.error("scraper failed" + str(e))
    finally:
        driver.quit()


def lookupApps(name, result_number):
    # do something interesting
    pass

if __name__ == "__main__":
    among_us = app_info.app_info("Amoung Us", "https://play.google.com/store/apps/details?id=com.innersloth.spacemafia", "", dt.date.today)
    reviews = getReviews(among_us, 10)
