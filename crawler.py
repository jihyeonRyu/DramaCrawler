from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import csv

loginURL = "https://db.kocca.kr/db/member/loginPage.do?menuNo=203303"
listURL = "http://db.kocca.kr/db/broadcastdb/scriptList.do"
driver = None

## chrome webdriver가 설치 되어 있어야 함
def login():
    global driver
    # 로그인 정보(아이디, 비밀번호) 가져오기
    f = open('./profile.csv', 'r')
    reader = csv.reader(f)
    profile = []
    for r in reader:
        profile.append(r)
    # 로그인 페이지 열기
    driver = webdriver.Chrome(executable_path='C:\\Users\\ryuji\\chromedriver\\chromedriver')
    driver.get(loginURL)
    # 키보드 보안 프로그램 설치 팝업 거부 및 확인
    if(Alert(driver)):
        Alert(driver).dismiss()
        Alert(driver).accept()
        Alert(driver).accept()
    # 로그인 정보 입력
    driver.find_element_by_id("userId").send_keys(profile[0])
    driver.find_element_by_id("password").send_keys(profile[1])
    driver.find_element_by_xpath('//*[@name="loginForm"]/div/fieldset/div/span/a').click()

def getDramaScript():
    # drama 대본 리스트
    global driver
    if driver is None:
        login()
    driver.get(listURL)
    driver.implicitly_wait(3)
    # 상세 검색 (드라마 선택)
    driver.find_element_by_class_name("toggle-title").click()
    driver.find_element_by_xpath('//label[@for="searchGenre0"]/input[@id="searchGenre0"]').click()
    driver.find_element_by_xpath('//table/tbody/tr/th/a/img[@alt="상세검색"]').click()
    # 드라마 목록 받아오기
    drama_links = [drama.get_attribute("href") for drama in driver.find_elements_by_xpath('//td[@class="left"]/a')]
    # paging
    page = [index.get_attribute("href") for index in driver.find_elements_by_xpath('//div[@class="paging"]/a')]
    for i in range(3, 11):
        driver.get(page[i])
        new_links = [drama.get_attribute("href") for drama in driver.find_elements_by_xpath('//td[@class="left"]/a')]
        for link in new_links:
            drama_links.append(link)

    print("드라마 갯수: %d" % (len(drama_links)))

    for link in drama_links:
        driver.get(link)
        script_btn = [btn for btn in driver.find_elements_by_xpath('//tr/td/a[@class="btn_look"]')]
        # 드라마 페이지 핸들러 저장
        drama_window_handle = None
        while not drama_window_handle:
            drama_window_handle = driver.current_window_handle

        for btn in script_btn:
            btn.click()     # 자바스크립트라서 클릭해야 가져올 수 있음
            # 팝업창의 핸들러 저장
            signin_window_handle = None
            while not signin_window_handle:
                for handle in driver.window_handles:
                    if handle != drama_window_handle:
                        signin_window_handle = handle
                        break
            driver.switch_to.window(signin_window_handle)
            outFile(driver.page_source)
            driver.close()
            driver.switch_to.window(drama_window_handle)

    driver.close()
    print("소스 파일 다운로드 완료!")


def outFile(source):
    bs = soup(source, 'html.parser')
    title = bs.find(id="title")
    f = open("./" + title + ".txt", 'wt')
    f.write(bs.string)
    f.close()

