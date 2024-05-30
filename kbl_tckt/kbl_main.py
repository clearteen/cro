from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.select import Select
from selenium.common.exceptions import WebDriverException
#from selenium.webdriver.common.action_chains import ActionChains
#import pyautogui

import time

#ID = input("ID: ")
#PW = input("PW: ")
#TEAM = input("구단(ex: https://egis.kbl.or.kr/): ")
#STADIUM = input("경기장(ex: 1): ")
#MATCH = input("경기(ex: 1): ")
ID = ''
PW = ''
TEAM = 'https://egis.kbl.or.kr/'
STADIUM = '1'
MATCH = '1'
#x = 366
#y = 422

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

def find(xpath) :
    return driver.find_element(By.XPATH, xpath)

driver = webdriver.Chrome(options=chrome_options)
#action = ActionChains(driver)

def safety(func, n=50):
    for _ in range(n):
        try:
            func()
            return
        except WebDriverException:
            time.sleep(0.01)
        except Exception:
            time.sleep(0.01)
    
    raise WebDriverException

def login():
    driver.get('https://www.kbl.or.kr/auth/login')
    find('//*[@id="container"]/div[1]/div[1]/ul/li[1]/input').send_keys(ID)
    find('//*[@id="container"]/div[1]/div[1]/ul/li[2]/input').send_keys(PW)
    find('//*[@id="container"]/div[1]/div[1]/ul/li[4]/button').click()

def select_match():
    time.sleep(1)
    safety(lambda: driver.get(TEAM)) #//*[@id="container"]/div/div[3]/div[1]/div[2]/div/div[1]/ul[1]/li[2]/text()
    safety(lambda: find(f'//*[@id="container"]/div/div[3]/div[1]/div[2]/div/div[{STADIUM}]/ul[3]/li[1]/button').click())
    stadium_xpath = find(f'//*[@id="container"]/div/div[3]/div[1]/div[2]/div/div[{STADIUM}]/ul[1]/li[2]')
    stadium_name = stadium_xpath.text
    print(stadium_name)
    safety(lambda: driver.switch_to.window(driver.window_handles[1]))
    #safety(lambda: find('//*[@id="scheduleListDiv"]/table/tbody/tr[1]/td[4]/a').click())
    #safety(lambda: find('//*[@id="noticeModalClose"]').click())
    while(True):
        try:
            safety(lambda: driver.refresh())
            safety(lambda: find(f'//*[@id="scheduleListDiv"]/table/tbody/tr[{MATCH}]/td[4]/a').click())
            safety(lambda: find('//*[@id="noticeModalClose"]').click())
            break
        except WebDriverException:
            print('refresh')
            time.sleep(0.01)

def select_seat():
    safety(lambda: find('//*[@id="seat_grade_87706"]/a').click())
    safety(lambda: find('//*[@id="seat_zone_114646"]/a').click())
    #safety(lambda: find('//*[@id="seat_grade_87714"]/a').click())
    #time.sleep(0.5)
    #safety(lambda: find('//*[@id="seat_zone_114625"]/a').click())
    
    '''time.sleep(1)
    left = pyautogui.locateOnScreen('left.png')
    pyautogui.click(pyautogui.center(left))
    #safety(lambda: action.move_to_element_with_offset(find('//*[@id="main_view"]/canvas[4]'), 366, 422).click().release().perform())
    safety(lambda: find('//*[@id="container"]/div[1]/div[2]/div[4]/a[2]').click())'''

login()
select_match()
#select_seat()
