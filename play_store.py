## SELENIUM
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


## MISC.
from datetime import datetime 
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
            f'review_details(\
                app_name={self.app_name}, \
                description={self.description}, \
                date={self.date}, \
                rating={self.rating}\
            )'
        )

def getReviews(app_details, reviewLimit):
    chrome_options = Options()  
    chrome_options.headless = True
    chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=chrome_options)
    wait = WebDriverWait(driver, 10)
    review_list = []
    try:
        driver.get(app_details.android_link + "&showAllReviews=true")
        lg.logger.warning("launched webdriver")
        assert "Among Us" in driver.title
         ## Switch to newest view first
        dropdown = driver.find_element_by_css_selector("div.MocG8c.UFSXYb.LMgvRb.KKjvXb")
        dropdown.click()
         # TODO stop making it rely on random sleep
        time.sleep(2)
        newest = driver.find_elements_by_css_selector("div.MocG8c.UFSXYb.LMgvRb")[3]
        newest.click()
         # TODO stop making it rely on random sleep
        time.sleep(3)
        reviews = driver.find_elements_by_css_selector("div[jscontroller='H6eOGe']")
        for review in reviews:
            if (len(review_list)) == reviewLimit:
                print(f'Reached review limit: {reviewLimit}')
                break
            r_desc = review.find_element_by_css_selector("div.UD7Dzf").text
            r_app_name = app_details.app_name
            temp_date = review.find_element_by_css_selector("span.p2TkOb").text
            r_date = datetime.strptime(temp_date, '%B %d, %Y').date()
            rating_wrapper = review.find_element_by_css_selector("span.nt2C1d")
            r_fullStars = len(rating_wrapper.find_elements_by_css_selector("div.vQHuPe.bUWb7c"))
            review_list.append(review_details(r_app_name, r_desc, r_date, r_fullStars))
            print(f'Added review {len(review_list)}/{reviewLimit}')   
    except NoSuchElementException as e:
        lg.logger.error("scraper failed" + str(e))
    finally:
        driver.quit()
    return review_list


def lookupApps(name, result_number):
    # do something interesting
    pass

if __name__ == "__main__":
    among_us = app_info.app_info("Amoung Us", "https://play.google.com/store/apps/details?id=com.innersloth.spacemafia", "", dt.date.today)
    reviews = getReviews(among_us, 40)
    for review in reviews:
        print(review)