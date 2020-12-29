from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import global_config

cfg = global_config.global_config.get_instance().CFG 

def create_chrome_driver():
    chrome_options = Options()  
    chrome_options.headless = cfg["selenium"]["headless"]
    driver = webdriver.Chrome(executable_path = cfg["selenium"]["driver_path"], options=chrome_options)
    return driver
