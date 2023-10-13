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


#리스트 정의
rec_newcomer = [] #신입
rec_career = [] #경력
rec_intern = [] #인턴
rec_pub = [] #채용공고 게시일
rec_dl = [] #마감일
cpn_name = [] #회사 이름
rec_field = [] #모집분야 (가구 디자인 관련 only)
cpn_kind = [] #가구 회사 종류 (인테리어, 가구 브랜드)
people = [] #직원 수
cpn_add = [] #회사 주소
project = [] #프로젝트 경향
recruit_url = [] #채용공고 url
cpn_url = [] #회사 url
cpn_sns = [] #회사 sns

recruit_career = [] #신입·경력·인턴 부분

#채용공고 url 수집하기
page = 5 #원하는 페이지 입력
for p in range(1,page+1): # 원하는 페이지까지 반복문
    
    # for문 안에 page_bar를 넣어주어 매번 지정
    page_bar = driver.find_elements(By.CSS_SELECTOR,'#dvGIPaging > div > ul > li > a')

    for button in page_bar:
        if button.text == str(p):
            button.click()
            break

    time.sleep(random.uniform(1,2))

    recruits = driver.find_elements(By.CSS_SELECTOR, "#dev-gi-list > div > div.tplList.tplJobList > table > tbody > tr > td > div > strong > a")

    #채용공고 필터링
    for recruit in recruits: 
        a = int('인테리어' in recruit.text) + int('가구' in recruit.text) + int('침구' in recruit.text)
        if a > 0:
            recruit_list = recruit.get_attribute("href")
            recruit_url.append(recruit_list)
    
    if p % 10 == 0:  # 10의 배수일때 다음10페이지 버튼 클릭
        driver.find_elements(By.CSS_SELECTOR,'#dvGIPaging > div > ul > li > a')[11].click()

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
        
    #신입·경력·인턴 부분
    text_crawling(recruit_career, By.CSS_SELECTOR, "#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(1) > dl > dd:nth-child(2)")
    
    #채용공고 게시일
    if len(driver.find_elements(By.CSS_SELECTOR, "#tab02 > div > article.artReadPeriod > div > dl.date > dd")) >= 2:
        text_crawling(rec_pub, By.CSS_SELECTOR, "#tab02 > div > article.artReadPeriod > div > dl.date > dd:nth-child(2) > span")
    else:
        rec_pub.append("확인 필요!")
    
    #마감일
    if len(driver.find_elements(By.CSS_SELECTOR, "#tab02 > div > article.artReadPeriod > div > dl.date > dd")) >= 2:
        text_crawling(rec_dl, By.CSS_SELECTOR, "#tab02 > div > article.artReadPeriod > div > dl.date > dd:nth-child(4) > span")
    else:
        rec_dl.append("확인 필요!")
    
    #회사 이름
    text_crawling(cpn_name, By.CSS_SELECTOR, "#container > section > div.readSumWrap.clear > article > div.sumTit > h3 > div > span")
    #모집분야 (가구 디자인 관련 only)
    # text_crawling(rec_field)

    #가구 회사 종류 (인테리어, 가구 브랜드)
    # text_crawling(cpn_kind)

    #직원 수
    if len(driver.find_elements(By.CSS_SELECTOR, "#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div.tbCol.tbCoInfo > dl > dd")) >= 5:
        text_crawling(people, By.CSS_SELECTOR, "#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div.tbCol.tbCoInfo > dl > dd:nth-child(4) > span")
    else:
        people.append("확인 필요!")

    #회사 주소 - 지역이 여러개인 경우를 손봐야함
    text_crawling(cpn_add, By.CSS_SELECTOR, "#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(2) > dl > dd:nth-child(6) > a")

    #프로젝트 경향
    # text_crawling(project)

    #회사 url
    if len(driver.find_elements(By.CSS_SELECTOR, "#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div.tbCol.tbCoInfo > dl > dd")) >= 5:
        text_crawling(cpn_url, By.CSS_SELECTOR, "#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div.tbCol.tbCoInfo > dl > dd:nth-child(10) > span > a")
    else:   
        cpn_url.append("확인 필요!")

    #회사 sns
    # text_crawling(cpn_sns)

    print('채용공고 ' + str(len(recruit_url)) + '개 중 ' + str(num) + '번째 채용공고 확인 완료')
    if num % 10 == 0:
        print('남은 소요 시간 : ' + str(round(((len(recruit_url)-num)*20)/60)) + '분')

#신입 구분
for i in recruit_career:
    if "신입" in i:
        rec_newcomer.append('o')
    else:
        rec_newcomer.append('')

#경력 구분
for i in recruit_career:
    if '경력' in i:
        if len(i) == 12:
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
            rec_career.append('확인 필요!')
    else:
        rec_career.append('')
    
#인턴 구분
for i in recruit_career:
    if "인턴" in i:
        rec_intern.append('o')
    else:
        rec_intern.append('')


for i in cpn_name:
    rec_field.append('')
    cpn_kind.append('')
    project.append('')
    cpn_sns.append('')


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
                '회사 명':cpn_name, '모집분야':rec_field, '가구 회사 종류':cpn_kind, '직원 수':people, '위치':cpn_add, 
                '프로젝트 경향':project, '채용 링크':recruit_url, '회사 홈페이지':cpn_url, '회사 sns':cpn_sns})
worksheet.update([df.columns.values.tolist()] + df.values.tolist())