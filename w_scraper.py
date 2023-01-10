import undetected_chromedriver as uc
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from datetime import datetime 
import uuid as uid     # library for producing unique global ID's
import time 
import pandas as pd
import re


URL = "https://www.eacj.org/?page_id=4821"

def generate_id(results: list = None):
    # generate unique global id with UUID package.
    unique_id = []

    # loop through each record, creating a unique id
    for value in enumerate(results):
        uuidv4 = uid.uuid4()
        unique_id.append(str(uuidv4))

    return unique_id

def options(url_id, headless: str):

    options = ChromeOptions()
    ua = UserAgent()
    user_agent = ua.random
    print(user_agent)

    if headless == "yes":
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(f'user-agent={user_agent}')
    else:
        options.add_argument("--start-maximized")
        options.add_argument(f'user-agent={user_agent}')

    driver = uc.Chrome(options=options)
    driver.get(url_id)
    
    return driver

if __name__ == "__main__":

    driver = options(URL, "no")

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(By.XPATH, "//*[@id='navigation']"))
        print("Website initiated!")
    except:
        print("Time out! shutting down session")
        # driver.quit()

    counter = 2
 
    while True:

        hyperlinks = driver.find_element(By.XPATH, f"//*[@id='post-4821']/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/table/tbody/tr[{counter}]/td[2]/a")
        print(hyperlinks.text)
        hyperlinks.click()

        # try:
        #     WebDriverWait(driver, 20).until(EC.presence_of_element_located(By.CLASS_NAME, "entry-title"))
        # except:
        #     driver.quit()
        #     break

        current_time = datetime.now()
        date_time = datetime.timestamp(current_time)
        timestamp = datetime.fromtimestamp(date_time)
        str_date_time = timestamp.strftime("%d-%m-%Y, %H:%M:%S")
        match = re.search(r'(:?post-)[0-9]+', driver.page_source, re.IGNORECASE)  # matched string to match with page id

        case_number = driver.find_element(By.XPATH, f'//*[@id="{match.group(0)}"]/div[2]/table[1]/tbody/tr[1]/td[2]')
        respondant = driver.find_element(By.XPATH, f'//*[@id="{match.group(0)}"]/div[2]/table[1]/tbody/tr[3]/td[2]')
        complaintant = driver.find_element(By.XPATH, f'//*[@id="{match.group(0)}"]/div[2]/table[1]/tbody/tr[4]/td[2]')
        country = driver.find_element(By.XPATH, f'//*[@id="{match.group(0)}"]/div[2]/table[1]/tbody/tr[6]/td[2]/a')
        date_delivered = driver.find_element(By.XPATH, f'//*[@id="{match.group(0)}"]/div[2]/table[2]/tbody/tr[3]/td[2]')

        print(f'Scraped: {str_date_time}, case_number: {case_number.text}, Respondant: {respondant.text}, Complaintant: {complaintant.text}, Country: {country.text}')
        counter = counter+1
        driver.back()
        if counter > 6:
            break


    driver.quit()
