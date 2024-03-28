import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import math

s = Service("C:\\Users\\User\\Desktop\\ChromeDriver\\chromedriver.exe")
driver = webdriver.Chrome(service=s)
link = "https://coinmarketcap.com/headlines/news/"

driver.get(link)
driver.maximize_window()

time.sleep(3)

driver.find_element(By.XPATH, "//div[@class='sc-16r8icm-0 dnQWht']").click()

print("Which news do you want to scrape?")
print("Enter 0 to scrape news about all Cryptocurrencies.")
print("Enter 1 to scrape news about Bitcoin.")
print("Enter 2 to scrape news about Ethereum.")
print("Enter 3 to scrape news about Tether.")
print("Enter 4 to scrape news about USD Coin.")
print("Enter 5 to scrape news about BNB.")
print("Enter 6 to scrape news about Binance USD.")
print("Enter 7 to scrape news about Cardano.")
print("Enter 8 to scrape news about XPR.")
print("Enter 9 to scrape news about other Cryptocurrency")

number = int(input())

if number == 1:
    driver.find_element(By.ID, "react-select-2-option-0").click()
if number == 2:
    driver.find_element(By.ID, "react-select-2-option-1").click()
if number == 3:
    driver.find_element(By.ID, "react-select-2-option-2").click()
if number == 4:
    driver.find_element(By.ID, "react-select-2-option-3").click()
if number == 5:
    driver.find_element(By.ID, "react-select-2-option-4").click()
if number == 6:
    driver.find_element(By.ID, "react-select-2-option-5").click()
if number == 7:
    driver.find_element(By.ID, "react-select-2-option-6").click()
if number == 8:
    driver.find_element(By.ID, "react-select-2-option-7").click()
if number == 9:
    print("Enter the exact name of the Cryptocurrency you want to scrape:")
    crypto_name = input()
    input_element = driver.find_element(By.XPATH, "//div/div/input")
    input_element.send_keys(crypto_name)
    input_element.send_keys(Keys.ENTER)

# Variables needed:
counter = 0
old_counter = 0
headlines_list = []
body_texts_list = []
posted_by_list = []
post_times_list = []


currently_scraping = driver.find_element(By.TAG_NAME, "h2").text
print("Currently scraping news about: " + currently_scraping)

print("How many headlines do you want to scrape?")
headlines_target_count = int(input())

while True:
    # Slowly scrolling to the end of the page to counteract lazy loading:
    print("Loading the complete page (scrolling)...")
    body_element = driver.find_element(By.TAG_NAME, 'body')
    old_height = driver.execute_script('return document.body.scrollHeight')

    while True:
        body_element.send_keys((Keys.PAGE_DOWN))
        body_element.send_keys((Keys.PAGE_DOWN))
        body_element.send_keys((Keys.PAGE_DOWN))
        time.sleep(10)  # Changing sleep time helps with page not loading error.
        headlines = driver.find_elements(By.XPATH, "//a[@class='sc-1eb5slv-0 kLhpLY cmc-link']")
#        counter = 0
#        for headline in headlines:
#            counter += 1
        counter = len(headlines)
        print("Number of scraped headlines: ", counter)
        if counter >= headlines_target_count:
            break
    break


headlines = driver.find_elements(By.XPATH, "//a[@class='sc-1eb5slv-0 kLhpLY cmc-link']")
body_texts = driver.find_elements(By.XPATH, "//p[@class='sc-1eb5slv-0 hdUmWM']")
posted_bys = driver.find_elements(By.XPATH, "//span[@class='sc-1eb5slv-0 ehYyPC']")
post_times = driver.find_elements(By.XPATH, "//span[@class='sc-1t3hyg7-0 hTMYuT']")

print("Exporting data to CSV...")

for i in range(0, headlines_target_count):
    headlines_list.append(headlines[i].text)
    body_texts_list.append(body_texts[i].text)
    posted_by_list.append(posted_bys[i].text)
    post_times_list.append(post_times[i].text)

time.sleep(10)

# Creating a CSV file with the scraped data

all_data = pd.DataFrame(
    {'Headline': headlines_list, 'Body': body_texts_list, 'Posted By': posted_by_list, 'Time Posted': post_times_list})
all_data.to_csv('headlines_test_data.csv', index=False)

print("Export to CSV finished!")