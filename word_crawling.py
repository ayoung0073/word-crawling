from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By  # elements 접근 함수
from selenium.webdriver.common.keys import Keys  # elements 접근 함수
from bs4 import BeautifulSoup
import csv

import constant

with open('/Users/bagchaegyeong/Desktop/word_crawling.csv', 'w', newline='', encoding='utf-8-sig') as csv_file:
    word_writer = csv.writer(csv_file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    driver = webdriver.Chrome(ChromeDriverManager().install())
    word_writer.writerow(['용어', '예문'])
    words = [
        "스크럼", "스프린트", "애자일", "사일로", "피봇", "마일스톤", "린", "MVP"
    ]
    except_ws = [
        "의미", "용어", "표현", "한다", "라고", "합니다", "말한다", "말합니다", "란", "이란"
    ]
    try:
        for word in words:
            print("word: " + word)
            driver.get(constant.GOOGLE_URL)  # 구글을 접속한다.
            driver.implicitly_wait(constant.DEFAULT_WAIT_LOADING_SECONDS)  # 웹페이지의 로딩을 대기한다.

            element = driver.find_element(By.CLASS_NAME, "gLFyf")
            element.send_keys(constant.SEARCH_PREFIX + word)
            element.send_keys(Keys.ENTER)
            driver.implicitly_wait(constant.DEFAULT_WAIT_LOADING_SECONDS)

            html = driver.page_source  # 페이지 소스를 가져온다.
            soup = BeautifulSoup(html, constant.HTML_PARSER)  # html 파싱

            articles = driver.find_elements(By.CLASS_NAME, "LC20lb")
            for article in articles:
                try:
                    article.click()
                except Exception as exception:
                    print("exception 발생")
                    driver.back()
                    continue
                driver.implicitly_wait(3)
                html = driver.page_source
                soup = BeautifulSoup(html, constant.HTML_PARSER)
                text = soup.text.strip()

                if (text.find("예") > 0 or text.find("\"") > 0) and text.find(word) > 0:  # 예문이 포함되어 있는 링크인지 확인
                    lines = text.replace("\n", "").replace("“", ".").replace("\"", ".").split(".")
                    for line in lines:
                        Flag = 1
                        for except_w in except_ws:
                            # print(except_w)
                            if line.find(except_w) > 0:
                                Flag = 0
                                break
                        if line.find(word) > 0 and len(line) > 7 and line.find(' ') > 0 and Flag != 0:  # 예문 찾기
                            print(line)
                            word_writer.writerow([word, line])
                            print("="*60)
                        else:
                            pass
                driver.back()

    finally:
        driver.quit()
        pass

csv_file.close()
