from driver import Element, driver
from mycaptcha import solve_captcha
import time
from mysmtp import send_email

ID = ""
PW = ""
SECTOR = "001"

web = Element()


def login():
    web.url("https://ticket.interpark.com/Gate/TPLogin.asp")
    web.iframe("first")
    web.find(id="userId").send_keys(ID)
    web.find(id="userPwd").send_keys(PW)
    web.find(id="btn_login").click()


def select_event():
    web.url("https://tickets.interpark.com/goods/24002990?app_tapbar_state=hide&")
    web.find(
        raw='//*[@id="productSide"]/div/div[1]/div[1]/div[2]/div/div/div/div/ul[3]/li[36]'
    ).click()
    web.find(text="예매하기").parent().click()


def pass_captcha():
    web.new_window()
    web.iframe("ifrmSeat")
    while True:
        web.find(raw='//*[@id="divRecaptcha"]/div[1]/div[4]/a')
        driver.execute_script("fnCapchaRefresh()")
        shot = web.uncertain(lambda: web.find(id="imgCaptcha").screenshot())
        if not shot:
            break
        answer = solve_captcha(shot, 1)
        web.find(raw='//*[@id="divRecaptcha"]/div[1]/div[3]').click()
        web.find(id="txtCaptcha").send_keys(answer)


def select_seat():
    web.find(text="Floor 스탠딩").parent().click()
    web.set_wait_until(timeout=0.3, freq=0.01)

    while True:
        web.uncertain(lambda: pass_captcha())
        """slider = web.uncertain(lambda: web.find(css_class="captchSliderLayer"))
        if slider:
            print("fail")
            return False"""

        web.iframe("default", "ifrmSeat")
        driver.execute_script("fnBlockSeatUpdate('', '', '001')")
        web.iframe("ifrmSeatDetail")
        seat = web.uncertain(lambda: web.find(tag="span", name="Seats"))
        if seat:
            seat.click()
            web.iframe("default", "ifrmSeat")
            driver.execute_script("fnSelect();")
            return True


login()
while True:
    web.set_wait_until(timeout=5, freq=0.1)
    try:
        select_event()
        pass_captcha()
        if select_seat():
            send_email()
            time.sleep(10000)
    except Exception:
        time.sleep(1)
    finally:
        try:
            web.back_window()
        except:
            pass
