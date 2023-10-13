from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

random_sec = random.uniform(3,5)

chrome_options = webdriver.ChromeOptions()

chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
driver.get("https://www.jobkorea.co.kr/")


time.sleep(3)

driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div[2]/div/a').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="devSearchForm"]/div[2]/div/div[1]/dl[1]/dt/p')))
driver.find_element(By.XPATH, '//*[@id="devSearchForm"]/div[2]/div/div[1]/dl[1]/dt/p').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lb_job_sch"]')))
driver.find_element(By.XPATH, '//*[@id="lb_job_sch"]').send_keys('가구디자인')
driver.find_element(By.XPATH, '//*[@id="lb_job_sch"]').send_keys('\n')
time.sleep(random_sec)
driver.find_element(By.XPATH, '//*[@id="devSearchForm"]/div[2]/div/div[1]/dl[1]/dd[2]/div[1]/div/div/dl/dd/div[1]/ul/li[1]/label/span/span').click()
driver.find_element(By.XPATH, '//*[@id="devSearchForm"]/div[2]/div/div[1]/dl[1]/dd[2]/div[1]/div/div/dl/dd/div[1]/ul/li[2]/label/span/span').click()
driver.find_element(By.XPATH, '//*[@id="devSearchForm"]/div[2]/div/div[1]/dl[1]/dd[2]/div[1]/div/div/dl/dd/div[1]/ul/li[3]/label/span/span').click()
driver.find_element(By.XPATH, '//*[@id="devSearchForm"]/div[2]/div/div[1]/dl[1]/dd[2]/div[1]/div/div/dl/div/button[2]').click()
time.sleep(random_sec)
driver.find_element(By.XPATH, '//*[@id="dev-btn-search"]').click()
time.sleep(random_sec)

recruit_url_messy = []

time.sleep(3)

recruits = driver.find_elements(By.CSS_SELECTOR, "#dev-gi-list > div > div.tplList.tplJobList > table > tbody > tr > td > div > strong > a")
for recruit in recruits:
    a = int('인테리어' in recruit.text) + int('가구' in recruit.text) + int('침구' in recruit.text)
    if a > 0:
        recruit_list = recruit.get_attribute("href")
        recruit_url_messy.append(recruit_list)
        print(recruit.text)
    
# for i in recruit_url_messy:
#     print(i)




