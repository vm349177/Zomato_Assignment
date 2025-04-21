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
    for k in range(2):
        # print("k:", k+1)
        categories = driver.find_elements(By.XPATH, '/html/body/div[2]/main/section[2]/div/div/section[1]/div[2]/div/div['+str(k+1)+']/section/div/h2')
        for i,category in enumerate(categories):
            # print("category:",i+1)
            category_name = category.text
            cards = driver.find_elements(By.XPATH, '/html/body/div[2]/main/section[2]/div/div/section[1]/div[2]/div/div['+str(k+1)+']/section['+str(i+1)+']/ul/li')
            print("no. of cards:", len(cards))
            for j in range(len(cards)):
                # print("card:",j+1)
                item_name = driver.find_element(By.XPATH, '/html/body/div[2]/main/section[2]/div/div/section[1]/div[2]/div/div['+str(k+1)+']/section['+str(i+1)+']/ul/li['+str(j+1)+']/div[1]/p').text
                item_tags = driver.find_element(By.XPATH, '/html/body/div[2]/main/section[2]/div/div/section[1]/div[2]/div/div['+str(k+1)+']/section['+str(i+1)+']/ul/li['+str(j+1)+']/p[2]/small').text
                tags = item_tags.split(', ')
                products_ct.append({
                    'company name': company_name,
                    'company location': company_location,
                    'company outlet': company_outlet,
                    'category': category_name,
                    'food items': item_name,
                    'tags': tags
                })

start = time.time()
url = "https://www.chaiatacos.com/menu/"
path = r"C:\Program Files\chromedriver-win64\chromedriver.exe"
driver = webdriver.Chrome(options = options, service= Service(path))
driver.set_page_load_timeout(10)
driver.get(url)
company_name = "Chaia Tacos"
company_location = ["3207 Grace Street, NW, Washington, DC 20007", "615 I St NW, Washington, DC 20001"]
company_outlet = ["Dining","Delivery","Pickup"]
products_ct = []
scrape()

df = pd.DataFrame(products_ct)
df.to_csv("products_chaiatacos.csv")



driver.quit()
end = time.time()
