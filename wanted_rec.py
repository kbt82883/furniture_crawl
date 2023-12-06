from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()

chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
driver.get("https://www.wanted.co.kr/jobsfeed")

#원티드에서 가구디자이너 채용공고 검색하기
time.sleep(3)
driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/nav/ul/li[1]/a/span').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[3]/article/div/div[1]/button/span[2]')))
driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/article/div/div[1]/button/span[2]').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[3]/article/div/div[1]/section/ul/li[4]/a')))
driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/article/div/div[1]/section/ul/li[4]/a').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[3]/article/div/div[2]/button/span[2]')))
driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/article/div/div[2]/button/span[2]').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[3]/article/div/div[2]/section/div[1]/div//*[contains(text(),"가구")]')))
driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/article/div/div[2]/section/div[1]/div//*[contains(text(),"가구")]').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[3]/article/div/div[2]/section/div[2]/button/span[2]')))
driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/article/div/div[2]/section/div[2]/button/span[2]').click()
time.sleep(2)

#리스트 정의
rec_newcomer = [] #신입
rec_career = [] #경력
rec_intern = [] #인턴
rec_pub = [] #채용공고 게시일
rec_dl = [] #마감일
cpn_name = [] #회사 이름
cpn_kind = [] #가구 회사 종류 (인테리어, 가구 브랜드)
people = [] #직원 수
cpn_add = [] #회사 주소
recruit_url = [] #채용공고 url
cpn_url = [] #회사 url

rec_title = []
cpn_add_messy = []
recruit_career = [] #신입·경력·인턴 부분
rec_pub_messy = []
rec_dl_messy = []

#스크롤 끝까지 내리기
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break
    last_height = new_height

#채용공고 url 수집하기
recruits = driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/div/ul/li/div/a')
for recruit in recruits:
    recruit_list = recruit.get_attribute("href")
    recruit_url.append(recruit_list)

print('크롤링 할 채용공고의 개수는 ' + str(len(recruit_url)) + '개 입니다')
# print('예상 소요 시간 : ' + str(round((len(recruit_url)*6)/60)) + '분')

#url에 접속해서 회사 채용정보 추출
def text_crawling(list, selector, elm):
    list.append(driver.find_element(selector, elm).text)

num = 0    

for recruit_crawl in recruit_url:
    driver.get(recruit_crawl)
    time.sleep(1)
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    
    num = num + 1

    #채용공고 제목
    text_crawling(rec_title, By.XPATH, '//*[@id="__next"]/div[3]/div[1]/div[1]/div[1]/section[2]/h2')

    #회사 이름
    text_crawling(cpn_name, By.XPATH, '//*[@id="__next"]/div[3]/div[1]/div[1]/div[1]/section[2]/div[1]/h6/a')

    #회사 주소
    text_crawling(cpn_add_messy, By.XPATH, '//*[@id="__next"]/div[3]/div[1]/div[1]/div[1]/div[2]/section[2]/div[2]/span[2]')

    #마감일
    text_crawling(rec_dl_messy, By.XPATH, '//*[@id="__next"]/div[3]/div[1]/div[1]/div/div[2]/section[2]/div[1]/span[2]')

    print('채용공고 ' + str(len(recruit_url)) + '개 중 ' + str(num) + '번째 채용공고 확인 완료')
    # if num % 10 == 0:
    #     print('남은 소요 시간 : ' + str(round(((len(recruit_url)-num)*6)/60)) + '분')

#채용 마감일 필터링
for i in rec_dl_messy:
    if i in '상시':
        rec_dl.append('상시 채용')
    elif i.startswith('20'):
        rec_dl.append(i[5:7] + '월 ' + i[8:10] + '일')
    else:
        rec_dl.append('확인 필요!')

        

#회사 주소 00 00구 형태로 변환
for i in cpn_add_messy:
    a = i.split()
    cpn_add.append(a[0] + " " + a[1])


#스프레드 시트에 작성----------------------------
import gspread
from pandas import DataFrame

# json 파일이 위치한 경로를 값으로 줘야 합니다.
json_file_path = "furnitures-recruit-automation-5da954d2f389.json"
gc = gspread.service_account(json_file_path)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1ygo_XrS4p6bD5nD6ozG20NLz3NmVRn9u5JlM7rNuatY/edit?usp=sharing"
doc = gc.open_by_url(spreadsheet_url)

worksheet = doc.worksheet("원티드 크롤링") #작성하려는 시트를 기입

df = DataFrame({'채용 마감일':rec_dl, '회사 이름':cpn_name, '회사 주소': cpn_add, '채용 링크':recruit_url})
worksheet.update([df.columns.values.tolist()] + df.values.tolist())

print('구글 시트 작성 완료')