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

#잡코리아에서 가구디자인 채용공고 검색하기
time.sleep(3)
driver.find_element(By.XPATH, '//*[@id="common_search_btn"]').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search"]/div/div/div[1]/div[3]/div[1]/button')))
driver.find_element(By.XPATH, '//*[@id="search"]/div/div/div[1]/div[3]/div[1]/button').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lb_job_sch"]')))
driver.find_element(By.XPATH, '//*[@id="lb_job_sch"]').send_keys('가구디자인')
driver.find_element(By.XPATH, '//*[@id="lb_job_sch"]').send_keys('\n')
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="search"]/div/div/div[1]/div[3]/div[2]/div[1]/div/div/div/dl/dd/div[1]/ul/li[1]/label/span/span').click()
driver.find_element(By.XPATH, '//*[@id="search"]/div/div/div[1]/div[3]/div[2]/div[1]/div/div/div/dl/dd/div[1]/ul/li[2]/label/span/span').click()
driver.find_element(By.XPATH, '//*[@id="search"]/div/div/div[1]/div[3]/div[2]/div[1]/div/div/div/dl/dd/div[1]/ul/li[3]/label/span/span').click()
driver.find_element(By.XPATH, '//*[@id="search"]/div/div/div[1]/div[3]/div[2]/div[1]/div/div/div/div/button[2]').click()
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="lb_job_sch"]').send_keys('인테리어디자인')
driver.find_element(By.XPATH, '//*[@id="lb_job_sch"]').send_keys('\n')
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="search"]/div/div/div[1]/div[3]/div[2]/div[1]/div/div/div/dl/dd/div[1]/ul/li[1]/label/span/span').click()
driver.find_element(By.XPATH, '//*[@id="search"]/div/div/div[1]/div[3]/div[2]/div[1]/div/div/div/dl/dd/div[1]/ul/li[2]/label/span/span').click()
driver.find_element(By.XPATH, '//*[@id="search"]/div/div/div[1]/div[3]/div[2]/div[1]/div/div/div/div/button[2]').click()
time.sleep(2)
driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[3]/div[2]/div[3]/div/dl[1]/dd[2]/button').click()
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div[2]/div[1]/div/button').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div[2]/div[1]/div/div/ul/li[2]/button').click()
time.sleep(random_sec)


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
rec_title_messy = []
recruit_career = [] #신입·경력·인턴 부분
rec_pub_messy = []
rec_dl_messy = []

#채용공고 url 수집하기
page = 12 #원하는 페이지 입력
for p in range(1,page+1): # 원하는 페이지까지 반복문
    
    # for문 안에 page_bar를 넣어주어 매번 지정
    page_bar = driver.find_elements(By.XPATH,'//*[@id="content"]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/ul/li/a')

    for button in page_bar:
        if button.text == str(p):
            button.click()
            break

    time.sleep(random.uniform(1,2))

    recruits = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div[2]/div[2]/div/div[1]/ul/li/div/div[2]/a')

    #채용공고 필터링
    for recruit in recruits: 
        a = int('인테리어' in recruit.text) + int('가구' in recruit.text) + int('침구' in recruit.text)
        if a > 0:
            recruit_list = recruit.get_attribute("href")
            recruit_url.append(recruit_list)
    
    # if p % 10 == 0:  # 10의 배수일때 다음10페이지 버튼 클릭
    #     driver.find_elements(By.CSS_SELECTOR,'#dvGIPaging > div > ul > li > a')[11].click()

print('크롤링 할 채용공고의 개수는 ' + str(len(recruit_url)) + '개 입니다')
print('예상 소요 시간 : ' + str(round((len(recruit_url)*20)/60)) + '분')

# #1페이지만 수집
# recruits = driver.find_elements(By.CSS_SELECTOR, "#dev-gi-list > div > div.tplList.tplJobList > table > tbody > tr > td > div > strong > a")

# #채용공고 필터링
# for recruit in recruits: 
#     a = int('인테리어' in recruit.text) + int('가구' in recruit.text) + int('침구' in recruit.text)
#     if a > 0:
#         recruit_list = recruit.get_attribute("href")
#         recruit_url.append(recruit_list)

#url에 접속해서 회사 채용정보 추출
def text_crawling(list, selector, elm):
    list.append(driver.find_element(selector, elm).text)

num = 0

for recruit_crawl in recruit_url:
    driver.get(recruit_crawl)
    time.sleep(random.uniform(18,22))
    
    num = num + 1
    # if num % 3 == 0:
    #     time.sleep(random.uniform(10,11))
    # else:
    #     time.sleep(random.uniform(5,6))
    
    #html inside html 키워드로 필터링
    # driver.switch_to.frame("gib_frame")
    # key_01 = driver.find_elements(By.XPATH, '//*[contains(text(),"인테리어")]')
    # key_02 = driver.find_elements(By.XPATH, '//*[contains(text(),"가구")]')
    # key_03 = driver.find_elements(By.XPATH, '//*[contains(text(),"가구디자인")]')
    # key_04 = driver.find_elements(By.XPATH, '//*[contains(text(),"가구 디자인")]')
    # key_05 = driver.find_elements(By.XPATH, '//*[contains(text(),"가구디자이너")]')
    # key_06 = driver.find_elements(By.XPATH, '//*[contains(text(),"가구 디자이너")]')
    # key_07 = driver.find_elements(By.XPATH, '//*[contains(text(),"가구설계")]')
    # key_08 = driver.find_elements(By.XPATH, '//*[contains(text(),"가구 설계")]')
    # key_09 = driver.find_elements(By.XPATH, '//*[contains(text(),"침구")]')
    # driver.switch_to.default_content()
    # if len(key_01) + len(key_02) + len(key_03) + len(key_04) + len(key_05) + len(key_06) + len(key_07) + len(key_08) + len(key_09) > 0:
        
    #채용공고 제목
    text_crawling(rec_title_messy, By.XPATH, '//*[@id="container"]/section/div[1]/article/div[1]/h3')
    # print(driver.find_element(By.XPATH,'//*[@id="container"]/section/div[1]/article/div[1]/h3').text)

    #신입·경력·인턴 부분
    if len(driver.find_element(By.CSS_SELECTOR, "#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(1) > dl > dd:nth-child(2)").text) > 1:
        text_crawling(recruit_career, By.CSS_SELECTOR, "#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(1) > dl > dd:nth-child(2)")
    else:
        recruit_career.append("확인 필요!")
    
    #채용공고 게시일
    if len(driver.find_elements(By.CSS_SELECTOR, "#tab02 > div > article.artReadPeriod > div > dl.date > dd")) >= 2:
        text_crawling(rec_pub_messy, By.CSS_SELECTOR, "#tab02 > div > article.artReadPeriod > div > dl.date > dd:nth-child(2) > span")
    else:
        rec_pub_messy.append("확인 필요!")
    
    #마감일
    if len(driver.find_elements(By.CSS_SELECTOR, "#tab02 > div > article.artReadPeriod > div > dl.date > dd")) >= 2:
        text_crawling(rec_dl_messy, By.CSS_SELECTOR, "#tab02 > div > article.artReadPeriod > div > dl.date > dd:nth-child(4) > span")
    else:
        rec_dl_messy.append("확인 필요!")
    
    #회사 이름
    text_crawling(cpn_name, By.CSS_SELECTOR, "#container > section > div.readSumWrap.clear > article > div.sumTit > h3 > div > span")

    #직원 수
    if len(driver.find_elements(By.CSS_SELECTOR, "#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div.tbCol.tbCoInfo > dl > dd")) >= 5:
        text_crawling(people, By.CSS_SELECTOR, "#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div.tbCol.tbCoInfo > dl > dd:nth-child(4) > span")
    else:
        people.append("-")

    #회사 주소 - 지역이 여러개인 경우를 손봐야함
    text_crawling(cpn_add, By.CSS_SELECTOR, "#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(2) > dl > dd > a")

    #회사 url
    if len(driver.find_elements(By.CSS_SELECTOR, "#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div.tbCol.tbCoInfo > dl > dd")) >= 5:
        text_crawling(cpn_url, By.CSS_SELECTOR, "#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div.tbCol.tbCoInfo > dl > dd:nth-child(10) > span > a")
    else:   
        cpn_url.append("-")

    print('채용공고 ' + str(len(recruit_url)) + '개 중 ' + str(num) + '번째 채용공고 확인 완료')
    if num % 10 == 0:
        print('남은 소요 시간 : ' + str(round(((len(recruit_url)-num)*20)/60)) + '분')

#신입 구분
for i in recruit_career:
    if "신입" in i:
        rec_newcomer.append('o')
    else:
        rec_newcomer.append('-')

#경력 구분
for i in recruit_career:
    if '경력' in i:
        if len(i) >= 12:
            rec_career.append(i[7])
        elif len(i) == 10:
            rec_career.append(i[4:6])
        elif len(i) == 9:
            rec_career.append(i[4])
        elif len(i) == 5:
            rec_career.append('확인 필요!')
        elif len(i) == 4:
            rec_career.append('무관')
        elif len(i) == 2:
            rec_career.append('무관')
    else:
        rec_career.append('-')
    
#인턴 구분
for i in recruit_career:
    if "인턴" in i:
        rec_intern.append('o')
    else:
        rec_intern.append('-')

#게시일 마감일 00월 00일로 변환
for i in rec_pub_messy:
    if i == '확인 필요!':
        rec_pub.append('확인 필요!')
    else:
        rec_pub.append(i[5:7] + '월 ' + i[8:10] + '일')

for i in rec_dl_messy:
    if i == '확인 필요!':
        rec_dl.append('확인 필요!')
    else:
        rec_dl.append(i[5:7] + '월 ' + i[8:10] + '일')

for i in rec_title_messy:
    rec_title.append(i[i.rfind('\n'):len(i)])

#가구 회사 종류
for i in rec_title:
    if '인테리어' in i:
        if ('시공' in i or '현장' in i) and ('설계' in i or '디자' in i):
            cpn_kind.append('종합 인테리어')
        elif '시공' in i or '현장' in i:
            cpn_kind.append('인테리어 시공')
        elif '설계' in i or '디자' in i:
            cpn_kind.append('인테리어 디자인')
        else:
            cpn_kind.append('확인 필요!')
    elif '가구' in i:
        cpn_kind.append('가구 브랜드')
    elif '침구' in i:
        cpn_kind.append('가구 브랜드')
    else:
        cpn_kind.append('확인 필요!')

print(len(rec_newcomer))
print(len(rec_career))
print(len(rec_intern))
print(len(rec_pub))
print(len(rec_dl))
print(len(cpn_name))
print(len(cpn_kind))
print(len(people))
print(len(cpn_add))
print(len(recruit_url))
print(len(cpn_url))

print(rec_title)

#스프레드 시트에 작성----------------------------
import gspread
from pandas import DataFrame

# json 파일이 위치한 경로를 값으로 줘야 합니다.
json_file_path = "furnitures-recruit-automation-5da954d2f389.json"
gc = gspread.service_account(json_file_path)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1ygo_XrS4p6bD5nD6ozG20NLz3NmVRn9u5JlM7rNuatY/edit?usp=sharing"
doc = gc.open_by_url(spreadsheet_url)

worksheet = doc.worksheet("잡코리아 크롤링") #작성하려는 시트를 기입

df = DataFrame({'신입':rec_newcomer, '경력':rec_career, '인턴':rec_intern, '채용공고 게시일':rec_pub, '채용 마감일':rec_dl, 
                '회사 명':cpn_name, '가구 회사 종류':cpn_kind, '직원 수':people, '위치':cpn_add, 
                '채용 링크':recruit_url, '회사 홈페이지':cpn_url})
worksheet.update([df.columns.values.tolist()] + df.values.tolist())

print('구글 시트 작성 완료')