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

    categories = driver.find_elements(By.XPATH, '//div[@class="food-menu-grid-item "]/section/div/h2')

    for i,category in enumerate(categories):
        category_name = category.text
        items = driver.find_elements(By.XPATH,'//div[@class="food-menu-grid-item "]['+str(i+1)+']/section/div/div/div')
        m = len(items)
        for j in range(m):
            name_xpath = '//div[@class="food-menu-grid-item "]['+str(i+1)+']/section/div/div/div['+str(j+1)+']/div[1]'
            price1_xpath = '//div[@class="food-menu-grid-item "]['+str(i+1)+']/section/div/div/div['+str(j+1)+']/div[2]'
            price2_xpath = '//div[@class="food-menu-grid-item "][' + str(i + 1) + ']/section/div/div/div[' + str(j + 1) + ']/div[3]'

            item_name = driver.find_element(By.XPATH,name_xpath).text
            if category_name == 'Curries (GF)':
                item_price1 = ""
            else:
                item_price1 = driver.find_element(By.XPATH, price1_xpath).text
            if len(driver.find_elements(By.XPATH, '//div[@class="food-menu-grid-item "][' + str(i + 1) + ']/section/div/div/div[' + str(j + 1) + ']/div')) >3:
                item_price2 = driver.find_element(By.XPATH, price2_xpath).text
                item_price = [item_price1, item_price2]
            else:
                item_price = [item_price1]
            print(item_name)
            print(item_price)
            tag_match = re.search(r'\(([A-Za-z,\s]+)\)\s*$', item_name)

            if tag_match:
                tags = [tag.strip() for tag in tag_match.group(1).split(',')]
                # Remove only the last set of parentheses (the tags) from the string
                dish_name = item_name[:tag_match.start()].strip()
            else:
                tags = []
                dish_name = item_name.strip()

            products_nasha.append({
                'restaurant': company_name,
                'address': company_location,
                'available on': company_outlet,
                'category': category_name,
                'item_name': dish_name,
                'tags': tags,
                'price': item_price
            })

    lunch_thali_button = driver.find_element(By.XPATH, '/html/body/div/main/article/div/div[1]/a[2]')
    lunch_thali_button.click()
    items = driver.find_elements(By.XPATH,'//div[@class="food-menu-grid-item  food-menu-grid-item--width2"]/section/div/div/div')
    for i in range(len(items)):
        item_name = driver.find_element(By.XPATH, '//div[@class="food-menu-grid-item  food-menu-grid-item--width2"]/section/div/div/div['+str(i+1)+']/div[1]').text
        item_price = driver.find_element(By.XPATH, '//div[@class="food-menu-grid-item  food-menu-grid-item--width2"]/section/div/div/div[' + str(i + 1) + ']/div[2]').text
        products_nasha.append({
            'company name': company_name,
            'company location': company_location,
            'available on': company_outlet,
            'category': 'Thali',
            'food item': item_name,
            'tags': [],
            'price': [item_price]
        })




start = time.time()
url = "https://downtown.nashaindia.com/austin-east-7th-nasha-food-menu"
path = r"C:\Program Files\chromedriver-win64\chromedriver.exe"
driver = webdriver.Chrome(options = options, service= Service(path))
driver.set_page_load_timeout(10)
driver.get(url)
company_name = "Nasha"
company_location = "1614 E 7th St, Austin, TX 78702, USA"
company_outlet = "Pickup, Delivery"
products_nasha = []
scrape()

df = pd.DataFrame(products_nasha)
df.to_csv("products_nasha.csv")



driver.quit()
end = time.time()