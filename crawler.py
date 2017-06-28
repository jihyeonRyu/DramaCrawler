from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.alert import Alert
import csv
import scriptParser

loginURL = "https://db.kocca.kr/db/member/loginPage.do?menuNo=203303"
listURL = "http://db.kocca.kr/db/broadcastdb/scriptList.do?menuNo=200462"
driver = None
num = 0

proxy = Proxy(
     {
          'proxyType': ProxyType.AUTODETECT
     }
)

def login():
    global driver
    # 로그인 정보(아이디, 비밀번호) 가져오기
    f = open('./profile.csv', 'r')
    reader = csv.reader(f)
    profile = []
    for r in reader:
        profile.append(r)
    # 로그인 페이지 열기
    desired_capabilities = webdriver.DesiredCapabilities.PHANTOMJS.copy()
    proxy.add_to_capabilities(desired_capabilities)
    driver = webdriver.PhantomJS(executable_path='C:\\Users\\ryuji\phantomjs-2.1.1-windows\\bin\\phantomjs', desired_capabilities=desired_capabilities)
    driver.get(loginURL)
    # 키보드 보안 프로그램 설치 팝업 거부 및 확인
    try:
        print("alert handling...")
        Alert(driver).dismiss()
        Alert(driver).accept()
        Alert(driver).accept()
    except:
        print("no alert")
    # 로그인 정보 입력
    driver.find_element_by_id("userId").send_keys(profile[0])
    driver.find_element_by_id("password").send_keys(profile[1])
    driver.find_element_by_xpath('//*[@name="loginForm"]/div/fieldset/div/span/a').click()

    print("login")


def get_drama_scripts():
    # drama 대본 리스트
    global driver

    if driver is None:
        login()

    driver.get(listURL)
    driver.implicitly_wait(10)
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
    print("the number of drama: %d" % (len(drama_links)))

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
            ebook_window_handle = None
            while not ebook_window_handle:
                for handle in driver.window_handles:
                    if handle != drama_window_handle:
                        ebook_window_handle = handle
                        break
            driver.switch_to.window(ebook_window_handle)
            out_file(driver.page_source)
            driver.close()
            driver.switch_to.window(drama_window_handle)

    driver.close()
    print("complete!")


def out_file(source):

    global num
    try:
        title, contents = scriptParser.get_contents(source)
        f = open(".\\data\\%s(%d).txt" % (title, num), 'wt', encoding="utf-8")
        f.write(contents)
        f.close()
        num = num + 1
        print("out %s file" % title)
    except:
        print("cannot out file")



