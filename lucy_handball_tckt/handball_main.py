from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.alert import Alert

import time

from mycaptcha import solve_captcha
#from mysmtp import send_email

ID = 'hl2dil'
PW = 'kb1211kb!'
YYMMDD = '001023'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

def find(xpath) :
    return driver.find_element(By.XPATH, xpath)

def find(xpath) :
    return driver.find_element(By.XPATH, xpath)


driver = webdriver.Chrome(options=chrome_options)

def safety(func, n=50) :
    for _ in range(n) :
        try :
            func()
            return
        except WebDriverException :
            time.sleep(0.01)
        except Exception :
            time.sleep(0.01)
    
    raise WebDriverException

def login():
    driver.get('https://ticket.interpark.com/Gate/TPLogin.asp')
    driver.switch_to.frame(find('//*[@id="loginAllWrap"]/div[2]/iframe'))
    find('//*[@id="userId"]').send_keys(ID)
    find('//*[@id="userPwd"]').send_keys(PW)
    find('//*[@id="btn_login"]').click()

def select_concert():
    driver.get('https://tickets.interpark.com/goods/24002990?app_tapbar_state=hide&')
    safety(lambda: find('//*[@id="productSide"]/div/div[1]/div[1]/div[2]/div/div/div/div/ul[3]/li[36]').click())
    find('//*[@id="productSide"]/div/div[2]/a[1]/span').click()

def safety_captcha():
    safety(lambda: driver.switch_to.window(driver.window_handles[1]))
    safety(lambda: driver.switch_to.frame(find('//*[@id="ifrmSeat"]')))
    while(True) :
        safety(lambda : find('//*[@id="divRecaptcha"]/div[1]/div[4]/a').is_displayed())
        if find('//*[@id="divRecaptcha"]/div[1]/div[4]/a').is_displayed() == True:
            safety(lambda : driver.execute_script('fnCapchaRefresh()'))
            safety(lambda : find('//*[@id="imgCaptcha"]').screenshot_as_png)
            answer = solve_captcha(find('//*[@id="imgCaptcha"]').screenshot_as_png, 1)
            safety(lambda : find('//*[@id="divRecaptcha"]/div[1]/div[3]').click())
            safety(lambda : find('//*[@id="txtCaptcha"]').send_keys(answer))
        else :
            break

def select_seat():
    safety(lambda: driver.switch_to.window(driver.window_handles[1]))
    safety(lambda: driver.switch_to.frame(find('//*[@id="ifrmSeat"]')))

    find('/html/body/form[1]/div/div[1]/div[3]/div/div[1]/div/div/div/div/table/tbody/tr[4]/td[1]/div/span[2]/strong').click()
    #safety(lambda: driver.switch_to.default_content())
    #safety(lambda: driver.switch_to.frame(find('//*[@id="ifrmSeat"]')))
    safety(lambda: find('//*[@id="GradeDetail"]/div/ul/li[9]/a').click())
    

login()
select_concert()
safety_captcha()
select_seat()