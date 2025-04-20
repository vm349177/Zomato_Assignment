import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_experimental_option('detach',True)

def scrape():
    view_all_buttons = driver.find_elements(By.XPATH, '//a[@class="elementor-button elementor-button-link elementor-size-sm"]')
    categories = driver.find_elements(By.XPATH, '//h2[@class="elementor-heading-title elementor-size-default"]')

    for i,view_all_button in enumerate(view_all_buttons):
        category_name = categories[i].text
        new_driver = webdriver.Chrome(options = options, service = Service(path))
        new_driver.set_page_load_timeout(10)
        new_url = view_all_button.get_attribute("href")
        new_driver.get(new_url)
        time.sleep(5)
        cards = new_driver.find_elements(By.XPATH, '//div[@data-elementor-type="loop-item"]')
        actions = ActionChains(new_driver)
        for card in cards:
            actions.move_to_element(card).perform()
            time.sleep(0.5)
        m = len(cards)
        for j in range(m):
            spice_xpath = '//div[@data-elementor-type="loop-item"]['+str(j+1)+']/div[1]/div/div/div/table/tbody/tr/td/p'
            name_xpath = '//div[@data-elementor-type="loop-item"]['+str(j+1)+']/div[2]/div[2]/div/div/a'
            with_xpath = '//div[@data-elementor-type="loop-item"]['+str(j+1)+']/div[3]/div/div/div'
            tags_xpath = '//div[@data-elementor-type="loop-item"]['+str(j+1)+']/div[4]/div/div/div/a'

            spice_level = new_driver.find_element(By.XPATH,spice_xpath).text
            product_name = new_driver.find_element(By.XPATH,name_xpath).text
            # print(product_name)
            try:
                product_with = new_driver.find_element(By.XPATH, with_xpath).text
            except Exception as e:
                product_with = ""
            tags = []
            try:
                product_tags = new_driver.find_elements(By.XPATH, tags_xpath)
                for tag in product_tags:
                    tags.append(tag.text)
            except Exception as e:
                pass
            products_cs.append({
                'company name': company_name,
                'company location': company_location,
                'available on': company_outlet,
                'category': category_name,
                'food item': product_name+" "+product_with,
                'spice level': spice_level,
                'tags': tags
            })
        new_driver.quit()





start = time.time()
url = "https://cafespice.com/foodservice/"
path = r"C:\Program Files\chromedriver-win64\chromedriver.exe"
driver = webdriver.Chrome(options = options, service= Service(path))
driver.set_page_load_timeout(10)
driver.get(url)
company_name = "Cafe Spice"
company_location = "677 Little Britain Road, New Windsor, NY"
company_outlet = "Amazon Fresh"
products_cs = []
scrape()

df = pd.DataFrame(products_cs)
df.to_csv("products_cafespice.csv")



driver.quit()
end = time.time()