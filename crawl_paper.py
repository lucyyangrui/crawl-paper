import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm

from lxml import etree

options = webdriver.ChromeOptions()
options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片
# options.add_argument('--headless')  # 不提供可视化页面
# 禁用浏览器弹窗
prefs = {
    'profile.default_content_setting_values':  {
        'notifications': 2
     }
}
options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome('./chromedriver.exe', options=options)


def main(key: str, url: str, begin: int, end: int):
    time.sleep(2)
    driver.get(url)
    time.sleep(random.randint(10, 12))
    driver.maximize_window()

    # 定位输入框 输入关键词
    input_table = driver.find_element(by=By.XPATH, value='//*[@id="completesearch-form"]/input')
    input_table.click()
    input_table.send_keys(key)
    time.sleep(5)

    # 开始爬取  下拉会自动刷新，首先下拉，获取到top篇文献为止
    paper_ele = []
    paper_info = []
    year = '0'
    # paper_info.append()

    while len(paper_ele) < end:
        ul_ele = driver.find_element(by=By.XPATH, value='//*[@id="completesearch-publs"]/div/ul')
        # //*[@id="journals/access/AlqudahKO23"]/cite/span[4]
        paper_ele = ul_ele.find_elements(by=By.XPATH, value='li')
        print(len(paper_ele))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    # page_source = driver.page_source
    # html = etree.HTML(page_source)
    for i, ele in enumerate(paper_ele):
        if i < begin:
            continue
        paper_info_tmp = []
        year_paper = ele.get_attribute('class')
        if 'entry' in year_paper:
            paper_info_tmp.append(year)
            # 获取期刊 / 会议
            meet_journal = ele.find_element(by=By.XPATH, value='div/img').get_attribute('title')
            if 'Journal' in meet_journal:
                paper_info_tmp.append('Journal')
            elif 'Conference' in meet_journal:
                paper_info_tmp.append('Conference')
            else:
                paper_info_tmp.append('Informal')

            title = ele.find_element(by=By.CLASS_NAME, value='title').text
            paper_info_tmp.append(title)
            source_url = ele.find_element(by=By.XPATH, value='cite/a').get_attribute('href')
            paper_info_tmp.append(source_url)
            paper_info.append(paper_info_tmp)
            time.sleep(1)
        else:
            year = ele.text
            print('===', year)
    print(paper_info[:2])
    print(len(paper_info))

    paper_info_end = []
    for i, paper in enumerate(paper_info):
        url = paper[-1]
        print(i, '==', url)
        if paper[1] != 'Informal':
            try:
                driver.execute_script("window.open('%s')" % url)
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)
                name = driver.find_element(by=By.XPATH, value='//*[@id="headline"]/h1').text
                name_t = name.split(',')[0]
                paper.append(name_t)
                paper_info_end.append(paper)
                time.sleep(2)
            except:
                paper.append('None')
                paper_info_end.append(paper)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    save_info = pd.DataFrame(paper_info_end, columns=['year', 'type', 'title', 'url', 'site'])
    save_info.to_csv('./paper_info.csv', index=False)


if __name__ == '__main__':
    main('multi-modal graph', 'https://dblp.org/', 0, 50)
    driver.close()
