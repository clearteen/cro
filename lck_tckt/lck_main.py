from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.alert import Alert

import time

from mycaptcha import solve_captcha
from mysmtp import send_email

ID = ''
PW = ''
YYMMDD = ''
MATCH = '/html/body/div[2]/div[4]/div[4]/div[1]/div[5]/a'
GOAL = 2
success = 0

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", False)

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

def select_match():
    driver.get('https://ticket.interpark.com/Contents/Sports/GoodsInfo?SportsCode=07032&TeamCode=PE015')
    find('//*[@id="div_checkDontsee_PT002_46_1"]/div[2]/button').click()
    find('//*[@id="div_checkDontsee_PT002_46_2"]/div[2]/button').click()
    safety(lambda: find(MATCH).click())
    
    safety(lambda: driver.switch_to.window(driver.window_handles[1]))
    safety(lambda: driver.switch_to.frame(find('//*[@id="ifrmSeat"]')))

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

def refresh_loop():
    while(True):
        safety(lambda: driver.refresh())
        safety(lambda: driver.switch_to.default_content())
        safety(lambda: driver.switch_to.frame(find('//*[@id="ifrmSeat"]')))
        safety_captcha()
        # 좌석 체크
        safety(lambda: find('/html/body/div[1]/div[3]/div[2]/div[1]'))
        left = find('/html/body/div[1]/div[3]/div[2]/div[1]/a')
        rc = left.get_attribute("rc")
        if rc != "0":
            left.click()
            return

def select_auto():
    refresh_loop()
    safety(lambda: find('/html/body/div[1]/div[3]/div[2]/div[1]/a').click())
    safety(lambda: find('/html/body/div[1]/div[3]/div[2]/div[3]/a[1]').click())

def select_price():
    safety(lambda: driver.switch_to.default_content())
    safety(lambda: driver.switch_to.frame(find('//*[@id="ifrmBookStep"]')))
    safety(lambda: Select(find('//*[@id="PriceRow000"]/td[3]/select')).select_by_value('1'))

    safety(lambda: driver.switch_to.default_content())
    #safety(lambda: driver.switch_to.window(driver.window_handles[1]))
    safety(lambda: find('//*[@id="SmallNextBtnImage"]').click())
    
    safety(lambda: driver.switch_to.default_content())
    #safety(lambda: driver.switch_to.window(driver.window_handles[1]))
    safety(lambda: driver.switch_to.frame(find('//*[@id="ifrmBookCertify"]')))
    safety(lambda: find('//*[@id="Agree"]').click())
    safety(lambda: find('//*[@id="information"]/div[2]/a[1]/img').click())
    
    safety(lambda: driver.switch_to.default_content())
    safety(lambda: find('//*[@id="SmallNextBtnImage"]').click())
    time.sleep(0.5)
    try:
        result = driver.switch_to.alert()
        safety(lambda: result.accept())
    except:
        pass

def back_auto():
    # 돌아가기 버튼
    driver.switch_to.default_content()
    driver.switch_to.frame(find('//*[@id="ifrmSeat"]'))
    find('/html/body/form[1]/div/div[1]/div[3]/div/div[4]/p[1]/a/img').click()

def check_me():
    safety(lambda: driver.switch_to.default_content())
    safety(lambda: driver.switch_to.frame(find('//*[@id="ifrmBookStep"]')))
    safety(lambda: find('//*[@id="Delivery"]').click())
    safety(lambda: find('//*[@id="YYMMDD"]').send_keys(YYMMDD))

    safety(lambda: driver.switch_to.default_content())
    safety(lambda: find('//*[@id="SmallNextBtnImage"]').click())

def alarm() :
    send_email()
    send_email()
    send_email()
    send_email()
    send_email()
    send_email()
    send_email()
    send_email()
    #time.sleep(1000)

#login()
#select_match()
#select_auto()
#select_price()
#check_me()

while(True):
    try :
        login()
        select_match()
        
        while(True) : 
            select_auto()
            try :
                select_price()
                break
            except WebDriverException :
                #좌석 선택 실패시 구역선택으로 다시 돌아가기
                back_auto()

        
        #check_me()
        success += 1
        #alarm()
        
    except WebDriverException :
        time.sleep(1)
    except Exception :
        time.sleep(1)
    finally :
        try :
            safety(lambda : driver.switch_to.window(driver.window_handles[0]))
        except WebDriverException :
            pass
        driver = webdriver.Chrome(options=chrome_options)
