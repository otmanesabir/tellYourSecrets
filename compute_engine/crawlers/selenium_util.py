from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'config')))
from config import global_config

cfg = global_config.global_config.get_instance().CFG 

def create_chrome_driver():
    chrome_options = Options()  
    chrome_options.headless = cfg["selenium"]["headless"]
    driver = webdriver.Chrome(executable_path = cfg["selenium"]["driver_path"], options=chrome_options)
    return driver
