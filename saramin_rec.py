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
driver.get("https://www.saramin.co.kr/zf_user/")

#사람인에서 가구디자인 채용공고 검색하기
time.sleep(3)
driver.find_element(By.XPATH, '//*[@id="btn_search"]').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search_form_recruit"]/div/div[3]/label')))
driver.find_element(By.XPATH, '//*[@id="search_form_recruit"]/div/div[3]/label').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="category_ipt_keyword"]')))
driver.find_element(By.XPATH, '//*[@id="category_ipt_keyword"]').send_keys('가구디자인')
driver.find_element(By.XPATH, '//*[@id="category_ipt_keyword"]').send_keys('\n')
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="panel_category"]/div[1]/div[1]/div/div[1]/div[2]/div/ul/li[1]/label').click()
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="btn_search_recruit"]').click()
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="recruit_info"]/div[2]/div/div[2]/button').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="recruit_info"]/div[2]/div/div[2]/div/ul/li[3]/button').click()
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

#채용공고 url 수집하기
page = 2 #원하는 페이지 입력
for p in range(1,page+1): # 원하는 페이지까지 반복문
    
    # for문 안에 page_bar를 넣어주어 매번 지정
    page_bar = driver.find_elements(By.CSS_SELECTOR,'#recruit_info_list > div.content_bottom > div > a')

    for button in page_bar:
        if button.text == str(p):
            button.click()
            break

    time.sleep(random.uniform(1,2))

    recruits = driver.find_elements(By.CSS_SELECTOR, "#recruit_info_list > div.content >div >div > h2 > a")

    #채용공고 필터링
    for recruit in recruits: 
        a = int('인테리어' in recruit.text) + int('가구' in recruit.text) + int('침구' in recruit.text)
        if a > 0:
            recruit_list = recruit.get_attribute("href")
            recruit_url.append(recruit_list)
    
    if p % 10 == 0:  # 10의 배수일때 다음10페이지 버튼 클릭
        driver.find_elements(By.CSS_SELECTOR,'#recruit_info_list > div.content_bottom > div > a')[11].click()

print('크롤링 할 채용공고의 개수는 ' + str(len(recruit_url)) + '개 입니다')
print('예상 소요 시간 : ' + str(round((len(recruit_url)*6)/60)) + '분')

# #1페이지만 수집
# recruits = driver.find_elements(By.CSS_SELECTOR, "#recruit_info_list > div.content >div >div > h2 > a")

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
    time.sleep(2)
    
    num = num + 1

    #채용공고 제목
    text_crawling(rec_title, By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[1]/div/h1')

    #신입·경력·인턴 부분
    text_crawling(recruit_career, By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[2]/div/div[1]/dl[1]/dd/strong')

    #채용공고 게시일
    if len(driver.find_elements(By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[6]/div/div/dl/dd')) >= 2:
        text_crawling(rec_pub_messy, By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[6]/div/div/dl/dd[1]')
    elif len(driver.find_elements(By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[5]/div/div/dl/dd')) >= 2:
        text_crawling(rec_pub_messy, By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[5]/div/div/dl/dd[1]')
    elif len(driver.find_elements(By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[4]/div/div/dl/dd')) >= 2:
        text_crawling(rec_pub_messy, By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[4]/div/div/dl/dd[1]')
    else:
        rec_pub_messy.append("확인 필요!")

    #마감일
    if len(driver.find_elements(By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[6]/div/div/dl/dd')) >= 2:
        text_crawling(rec_dl_messy, By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[6]/div/div/dl/dd[2]')
    elif len(driver.find_elements(By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[5]/div/div/dl/dd')) >= 2:
        text_crawling(rec_dl_messy, By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[5]/div/div/dl/dd[2]')
    elif len(driver.find_elements(By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[4]/div/div/dl/dd')) >= 2:
        text_crawling(rec_dl_messy, By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[4]/div/div/dl/dd[2]')
    else:
        rec_dl_messy.append("확인 필요!")

    #회사 이름
    text_crawling(cpn_name, By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[1]/div/div[1]/a[1]')

    #기업정보 페이지로 들어가기 (사람인 전용)
    if driver.find_element(By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[1]/div/div[1]/a[1]').get_attribute("href"):
        cpn_info_page = driver.find_element(By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[1]/div/div[1]/a[1]').get_attribute("href")
        driver.get(cpn_info_page)
        time.sleep(2)

        #직원 수
        try:
            text_crawling(people, By.XPATH, '//*[@id="content"]/div/div[3]/section[2]/div[2]/div/ul/li//*[contains(text(),"명")]')
        except:
            people.append('-')

        #회사 주소 - 지역이 여러개인 경우를 손봐야함
        cpn_info_list_elm = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div[3]/section[2]/div[2]/div/div/dl/div/dt')

        cpn_info_list = []
        for i in driver.find_elements(By.XPATH, '//*[@id="content"]/div/div[3]/section[2]/div[2]/div/div/dl/div/dt'):
            cpn_info_list.append(i.text)

        if '주소' in cpn_info_list:
            for i in cpn_info_list_elm:
                if '주소' == i.text:
                    cpn_add_index = int(driver.find_elements(By.XPATH, '//*[@id="content"]/div/div[3]/section[2]/div[2]/div/div/dl/div/dt').index(i)) + 1
                    text_crawling(cpn_add_messy, By.XPATH, '//*[@id="content"]/div/div[3]/section[2]/div[2]/div/div/dl/div[' + str(cpn_add_index) + ']/dd')
        else:
            cpn_add_messy.append('-')

        #회사 url
        if '홈페이지' in cpn_info_list:
            for i in cpn_info_list_elm:
                if '홈페이지' == i.text:
                    cpn_url_index = int(driver.find_elements(By.XPATH, '//*[@id="content"]/div/div[3]/section[2]/div[2]/div/div/dl/div/dt').index(i)) + 1
                    cpn_url.append(driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/section[2]/div[2]/div/div/dl/div[' + str(cpn_url_index) + ']/dd/a').get_attribute("href"))
        else:
            cpn_url.append('-')

    else:
        people.append('-')
        cpn_add_messy.append('-')
        cpn_url.append('-')

    print('채용공고 ' + str(len(recruit_url)) + '개 중 ' + str(num) + '번째 채용공고 확인 완료')
    if num % 10 == 0:
        print('남은 소요 시간 : ' + str(round(((len(recruit_url)-num)*6)/60)) + '분')

#신입 구분
for i in recruit_career:
    if "신입" in i:
        rec_newcomer.append('o')
    else:
        rec_newcomer.append('-')

#경력 구분
for i in recruit_career:
    if '경력' in i:
        rec_career.append('o')
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

print(len(cpn_add_messy))
print(cpn_add_messy)

#회사 주소 00 00구 형태로 변환
for i in cpn_add_messy:
    if i == '-':
        cpn_add.append('-')
    else:
        a = i.split()
        cpn_add.append(a[1] + " " + a[2])

#가구 회사 종류
for i in rec_title:
    if '인테리어' in i:
        cpn_kind.append('인테리어')
    elif '가구' in i:
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


#스프레드 시트에 작성----------------------------
import gspread
from pandas import DataFrame

# json 파일이 위치한 경로를 값으로 줘야 합니다.
json_file_path = "furnitures-recruit-automation-5da954d2f389.json"
gc = gspread.service_account(json_file_path)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1ygo_XrS4p6bD5nD6ozG20NLz3NmVRn9u5JlM7rNuatY/edit?usp=sharing"
doc = gc.open_by_url(spreadsheet_url)

worksheet = doc.worksheet("사람인 크롤링") #작성하려는 시트를 기입

df = DataFrame({'신입':rec_newcomer, '경력':rec_career, '인턴':rec_intern, '채용공고 게시일':rec_pub, '채용 마감일':rec_dl, 
                '회사 명':cpn_name, '가구 회사 종류':cpn_kind, '직원 수':people, '위치':cpn_add, 
                '채용 링크':recruit_url, '회사 홈페이지':cpn_url})
worksheet.update([df.columns.values.tolist()] + df.values.tolist())

print('구글 시트 작성 완료')