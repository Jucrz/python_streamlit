import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from pathlib import Path


crypto_token_list = ['BTC', 'ETH', 'SOL']


browser = webdriver.Chrome(r'C:\Users\jujuc\Chrome_driver\chromedriver_win32\chromedriver')

browser.get('https://coinmarketcap.com/')
time.sleep(3)

browser.maximize_window()
time.sleep(2)

cookies = browser.find_element_by_xpath('/html/body/div/div/div[1]/div[2]/div/div/div[5]/table/tbody/tr[1]/td[3]/div/a/div/div/p')
cookies.click()
time.sleep(3)
data_list = []
for crypto_token in crypto_token_list:
    search = browser.find_element_by_xpath('//*[@id="__next"]/div[1]/div[1]/div[1]/div[1]/div/div[2]/div[3]/div/div[1]')
    search.click()
    time.sleep(3)
    search = browser.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div/div/div/div[1]/div[1]/input')
    search.send_keys(crypto_token)
    time.sleep(3)

    cryptocurrencie = browser.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[1]/div[1]/div/div[2]/div[4]/div/div/div/div/div[2]/div[1]/a/div/div[2]')
    cryptocurrencie.click()
    time.sleep(3)


    data = browser.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[2]/div/div[2]/div/span/a[3]')
    data.click()
    time.sleep(3)

    daterange = browser.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[2]/div/div[3]/div[2]/div/div[1]/span/button')
    daterange.click()
    time.sleep(3)

    daterange = browser.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[2]/div/div[3]/div[2]/div/div[1]/div/div/div[1]/div/div/div[1]/div[2]/ul/li[5]')
    daterange.click()
    time.sleep(3)

    next_step = browser.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[2]/div/div[3]/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/span/button')
    next_step.click()
    time.sleep(3)

    data = browser.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[2]/div/div[3]/div[2]/div/div[2]/table/thead')
    data = data.text

    data = data.split(" ")

    test = browser.find_elements_by_tag_name('tr')
    header_df = "Date Open* High Low Close** Volume MarketCap"
    header_df2 = "Date Open* High Low Close** Volume Market Cap"
    if not data_list:
        data_list.append(header_df + " Crypto")
    for elem in test:
        if elem.text != test[0].text:
            if elem.text != header_df2:
                data_list.append(elem.text + " " + crypto_token)

    i = 1
    for elem in data_list[1::]:
        elem = " "+elem[0:10].replace(" ", "/")+data_list[i][10::]
        data_list[i] = elem
        i += 1
    print(data_list)


df = pd.DataFrame(data_list)

browser.close()

filepath = Path(r'C:\Users\jujuc\NoteBook\Python\CoinMarketCap.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(filepath)

df = pd.read_csv(r'C:\Users\jujuc\NoteBook\Python\CoinMarketCap.csv', sep=" ", header=1)
df.reset_index(drop=True, inplace=True)
df.rename(columns={"0,Date": "Date"}, inplace=True)
df.rename(columns={"Open*": "Open"}, inplace=True)
df.rename(columns={"Close**": "Close"}, inplace=True)
for col in df.columns:
    df[col] = df[col].replace({',': ''}, regex=True)
df["Volume"] = df["Volume"].replace({'"': ''}, regex=True)
df["Crypto"] = df["Crypto"].replace({'"': ''}, regex=True)
df = df.replace({'\$': ""}, regex=True)
df["Open"] = df["Open"].astype(float)
df["High"] = df["High"].astype(float)
df["Low"] = df["Low"].astype(float)
df["Close"] = df["Close"].astype(float)
df["Volume"] = df["Volume"].astype(float)
filepath = Path(r'C:\Users\jujuc\NoteBook\Python\CoinMarketCap.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(filepath)
