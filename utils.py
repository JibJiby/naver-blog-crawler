"""
블로그에 올라온 포스팅 앞부분 (후킹 중심으로 분석)

(나중)
제목에 들어간 키워드의 검색 수가 어떤지도 디테일 분석
"""
import os
import time

from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv(verbose=True)

blog_post_url = os.getenv('BLOG_URL')

def crawl_post(target_url: str):


    html = requests.get(target_url)
    soup = BeautifulSoup(html.text, 'html.parser')

    # 제목
    title = soup.select_one(".pcol1").text.strip()
    # print("제목 :", title)

    # 본문
    p_list = soup.select("p.se-text-paragraph")
    content = ""
    # print("==="*20, "내용", "==="*20)

    # content = "\n".join([p.text for p in p_list])
    for v in p_list[1:]:
        p = v.text.strip()
        content += p + '\n'
    # print(content)
    return content

def crawl_post_list(main_url: str, result_list: list):
    cwd_path = os.getcwd()
    webdriver_path = os.path.join(cwd_path, "webdriver", "chromedriver")
    print(webdriver_path)

    driver_option = webdriver.ChromeOptions()
    driver_option.add_argument('headless') # 창모드 끄기
    driver = webdriver.Chrome(webdriver_path, options=driver_option)
    driver.get(main_url)

    # 페이지 네이션 적용하기
    pagenate_el = driver.find_element_by_css_selector(".wrap_blog2_paginate .blog2_paginate ") # 클릭할 때마다 찾아줘야 한다. Session Id 바뀌기 때문.
    # pagenate_children_el = pagenate_el.find_elements_by_xpath("./*")[1:]
    num_pagenate = len(pagenate_el.find_elements_by_xpath("./*")[1:])
    for i in range(num_pagenate):
        if i==0:
            result_posts = get_now_page_list(driver)
            result_list.extend(result_posts)
        else:
            time.sleep(3) # 시간에 따라 오류가 났다가 안났다가 그런다. 네트워크 문제인듯. 명시적 wait하기 번거로워서 간단히 처리
            # 클릭 후 크롤링
            pagenate_el = driver.find_element_by_css_selector(".wrap_blog2_paginate .blog2_paginate")
            pagenate_children_el_list = pagenate_el.find_elements_by_xpath("./*")[1:]
            pagenate_children_el_list[i].click() # 올바르게 클릭한 거 맞음

            result_posts = get_now_page_list(driver)
            result_list.extend(result_posts)


    time.sleep(1)
    driver.close()





def get_now_page_list(driver: webdriver.Chrome) -> list:
    tmp_list = []
    # 현재 페이지에 보이는 포스트들 주소 가져오기
    table_el = driver.find_elements_by_css_selector(".wrap_list")
    result_post_list = table_el[0].find_elements_by_css_selector("td.title a")
    for e in result_post_list:
        # print(e.text, e.get_attribute("href"))
        tmp = {'title': e.text.strip(), 'href': e.get_attribute('href')}
        tmp_list.append(tmp)

    return tmp_list


def main():
    result_list = []
    crawl_post_list(blog_post_url, result_list)

    with open('data/result.csv', 'w', encoding='utf-8') as f:
        for v in result_list:
            f.writelines([v['title'],'\t' ,v['href'], '\n'])
            # print(v['title'], v['href'])
if __name__ == '__main__':
    main()