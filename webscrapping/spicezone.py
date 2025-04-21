import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_experimental_option('detach',True)

def scrape():
    categories = driver.find_elements(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div/div[2]/div[1]/div/h4/a')
    for i,category in enumerate(categories):
        # print("category:",i+1)
        category_name = category.text
        cards = driver.find_elements(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div/div[2]/div[1]/div/ul['+str(i+1)+']/li')
        # print("no. of cards:", len(cards))
        for j in range(len(cards)):
            # print("card:",j+1)
            item_name = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div/div[2]/div[1]/div/ul['+str(i+1)+']/li['+str(j+1)+']/div/div[1]/h4').text
            try:
                item_decription = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div/div[2]/div[1]/div/ul['+str(i+1)+']/li['+str(j+1)+']/div/div[1]/p[2]').text
            except Exception as e:
                item_decription = ""
            tags = re.findall(r'\((.*?)\)', item_decription)

            # Split combined tags like 'V,GF' into separate ones and deduplicate
            all_tags = set()
            for tag_group in tags:
                for tag in tag_group.split(','):
                    all_tags.add(tag.strip())
            products_sz.append({
                'restaurat': company_name,
                'address': company_location,
                'company outlet': company_outlet,
                'category': category_name,
                'item_name': item_name,
                'tags': tags
            })

start = time.time()
url = "https://spicezonewy.com/menus/"
path = r"C:\Program Files\chromedriver-win64\chromedriver.exe"
driver = webdriver.Chrome(options = options, service= Service(path))
driver.set_page_load_timeout(10)
driver.get(url)
company_name = "Spice Zone"
company_location = "600 W 19th St, Cheyenne, WY 82001, United States"
company_outlet = "Dining"
products_sz = []
scrape()

df = pd.DataFrame(products_sz)
df.to_csv("products_spicezone.csv")



driver.quit()
end = time.time()
