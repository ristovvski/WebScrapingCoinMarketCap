import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import math

s = Service("C:\\Users\\User\\Desktop\\ChromeDriver\\chromedriver.exe")
driver = webdriver.Chrome(service=s)

driver.maximize_window()

crypto_names = ["cirus-foundation",
"agoras-tokens",
"tokpie",
"multivac",
"doge-dash",
"stratos",
"nft-worlds",
"carbon-credit",
"bytecoin-bcn",
"unification",
"the-transfer-token",
"saffron-finance",
"hamster",
"gamee",
"dhedge-dao",
"reflexer-ungovernance-token",
"dogebonk",
"gameswap",
"atari-token",
"cardstack",
"sora",
"cache-gold",
"arsenal-fan-token",
"deri-protocol",
"ilcoin",
"muse",
"vempire-ddao",
"nakamoto-games",
"pac-protocol",
"vidya",
"triumphx",
"polkabridge",
"nexus",
"juggernaut",
"bitcny",
"dehub",
"revolt-2-earn",
"meetone",
"dfyn-network",
"raiden-network-token",
"e-money-coin",
"santiment",
"vesper",
"blockchain-brawlers",
"covesting",
"dovu",
"bao-finance",
"decimal",
"v-systems",
"dsla-protocol",
"govi",
"openocean",
"impossible-decentralized-incubator-access",
"monsta-infinite",
"poa",
"1world",
"defi-yield-protocol",
"now-token",
"opulous",
"bhp-coin",
"trabzonspor-fan-token",
"fenerbahce-token",
"zigcoin",
"ignis",
"salt",
"zookeeper",
"modefi",
"cumrocket",
"viacoin",
"gmcoin",
"minter-network",
"retreeb",
"ethax",
"populous",
"satt",
"safe-deal",
"nervenetwork",
"neighbourhoods",
"lithium",
"ufc-fan-token",
"defi-land",
"abyss",
"mint-club",
"safex-token",
"edgeless",
"green-satoshi-token-bsc",
"otocash",
"xend-finance",
"oraichain-token",
"factom",
"razor-network",
"monetha",
"jobchain",
"suterusu",
"karma"]


for crypto_name in crypto_names:
    link = "https://coinmarketcap.com/currencies/" + crypto_name + "/historical-data/"

    print("Currently scraping: " + crypto_name)

    driver.get(link)
    time.sleep(10)
    counter = 0
    old_counter = 0
    days_list = []
    opens_list = []
    highs_list = []
    lows_list = []
    volumes_list = []
    closes_list = []
    market_caps_list = []
    zastoj = 0
    flag = 1

    print("How many days do you want to scrape?")
    days_target_count = 500

    while True:
        if flag:
            # Slowly scrolling to the end of the page to counteract lazy loading:
            print("Loading the complete page (scrolling)...")
            body_element = driver.find_element(By.TAG_NAME, 'body')
            body_element.send_keys((Keys.PAGE_DOWN))
            time.sleep(3)
            body_element.send_keys((Keys.PAGE_DOWN))
            time.sleep(3)
            body_element.send_keys((Keys.PAGE_DOWN))
            time.sleep(5)
            flag = 0

        days = driver.find_elements(By.XPATH, "//tr/td[1]")

        counter = len(days)
        if counter == old_counter:
            zastoj = zastoj + 1
        else:
            zastoj = 0

        old_counter = counter
        if zastoj >= 10:
            break
        print("Number of scraped days: ", counter)
        if counter >= days_target_count:
            break

        if driver.find_elements(By.XPATH, "//button[@style='padding: 12px 95px;']"):
            time.sleep(3)
            button = driver.find_element(By.XPATH, "//button[@style='padding: 12px 95px;']")
            driver.execute_script("arguments[0].click();", button)
        else:
            print("All data scraped")
            break
    print("Scraped " + str(counter) + "days for crypto: " + crypto_name)
    days = driver.find_elements(By.XPATH, "//tr/td[1]")
    opens = driver.find_elements(By.XPATH, "//tr/td[2]")
    highs = driver.find_elements(By.XPATH, "//tr/td[3]")
    lows = driver.find_elements(By.XPATH, "//tr/td[4]")
    closes = driver.find_elements(By.XPATH, "//tr/td[5]")
    volumes = driver.find_elements(By.XPATH, "//tr/td[6]")
    market_caps = driver.find_elements(By.XPATH, "//tr/td[7]")

    print("Exporting data to CSV...")

    for i in range(0, counter - 1):
        days_list.append(days[i].text)
        opens_list.append(opens[i].text)
        highs_list.append(highs[i].text)
        lows_list.append(lows[i].text)
        closes_list.append(closes[i].text)
        volumes_list.append(volumes[i].text)
        market_caps_list.append(volumes[i].text)

    time.sleep(10)
    # Creating a CSV file with the scraped data

    all_data = pd.DataFrame(
        {'Day': days_list, 'Open': opens_list, 'High': highs_list, 'Low': lows_list,
         'Close': closes_list, 'Volume': volumes_list, 'Market Cap': market_caps_list})
    all_data.to_csv(crypto_name + '.csv', index=False)

    print("Export to CSV finished!")