import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# https://www.laugfssuper.com/index.php/categories/household.html
url = input('Enter url: ')
browser_driver = Service('C:/webdrivers/chromedriver.exe')
page_to_scrape = webdriver.Chrome(service=browser_driver)

page_to_scrape.get(url)

product_names = page_to_scrape.find_elements(By.CLASS_NAME, "product-name")
product_prices = page_to_scrape.find_elements(By.CLASS_NAME, "price")

file = open('laugfproducts.csv', 'w')
writer = csv.writer(file)
writer.writerow(["PRODUCT NAME", " PRICE"])

isNextDisabled = False
while not isNextDisabled:

    while True:
        product_names = page_to_scrape.find_elements(By.CLASS_NAME, "product-name")
        product_prices = page_to_scrape.find_elements(By.CLASS_NAME, "price")
        for product_name, product_price in zip(product_names, product_prices):
            writer.writerow(
                [product_name.text.encode('cp850', 'replace').decode('cp850').replace('?', ''), product_price.text])

            print(product_name.text.encode('cp850', 'replace').decode('cp850').replace('?',
                                                                                       '') + ', ' + product_price.text)
        try:
            page_to_scrape.find_element(By.CLASS_NAME, "next i-next").click()
        except NoSuchElementException:
            break
        file.close()
    try:
        l = WebDriverWait(page_to_scrape, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                '/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div[3]/div/ol/li[6]/a')))
        page_to_scrape.execute_script("arguments[0].click();", l)
    except:
        print('No more pages to load')
        break
