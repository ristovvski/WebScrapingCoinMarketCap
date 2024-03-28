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

crypto_names = ["Bitcoin", "Tether", "Ethereum"]


for crypto_name in crypto_names:

    driver.find_element(By.XPATH, "//div[@class='sc-16r8icm-0 dnQWht']").click()

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
    zastoj = 0
    trust_scores_list = []

    currently_scraping = driver.find_element(By.TAG_NAME, "h2").text
    print("Currently scraping news about: " + currently_scraping)

    print("How many headlines do you want to scrape?")
    headlines_target_count = 3500

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
            trust_scores = driver.find_elements(By.XPATH, "//p[@class='sc-14rfo7b-0 sc-1fbgneh-3 lNHNu' or @class='sc-14rfo7b-0 ezndLv' or @class='sc-14rfo7b-0 sc-1fbgneh-3 ZudXh']")

            counter = len(trust_scores)
            if counter == old_counter:
                zastoj = zastoj + 1
            else:
                zastoj = 0

            old_counter = counter
            if zastoj >= 10:
                break
            print("Number of scraped headlines: ", counter)
            if counter >= headlines_target_count:
                break
        break

    trust_scores = driver.find_elements(By.XPATH, "//p[@class='sc-14rfo7b-0 sc-1fbgneh-3 lNHNu' or @class='sc-14rfo7b-0 ezndLv' or @class='sc-14rfo7b-0 sc-1fbgneh-3 ZudXh']")
    headlines = driver.find_elements(By.XPATH, "//a[@class='sc-1eb5slv-0 kLhpLY cmc-link']")
    body_texts = driver.find_elements(By.XPATH, "//p[@class='sc-1eb5slv-0 hdUmWM']")
    posted_bys = driver.find_elements(By.XPATH, "//span[@class='sc-1eb5slv-0 iworPT']")
    post_times = driver.find_elements(By.XPATH, "//p[@class='sc-1eb5slv-0 bdsEAQ']")

    print("Exporting data to CSV...")

    for i in range(0, counter - 1):
        headlines_list.append(headlines[i].text)
        body_texts_list.append(body_texts[i].text)
        posted_by_list.append(posted_bys[i].text)
        post_times_list.append(post_times[i].text)
        cela = trust_scores[i].text
        trust_scores_list.append(cela[2:])

    time.sleep(10)
    body_element.send_keys(Keys.HOME)
    # Creating a CSV file with the scraped data

    all_data = pd.DataFrame(
        {'Headline': headlines_list, 'Body': body_texts_list, 'Posted By': posted_by_list, 'Time Posted': post_times_list, 'Trust Score': trust_scores_list})
    all_data.to_csv(crypto_name + '.csv', index=False)

    print("Export to CSV finished!")