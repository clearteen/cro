from driver import Element, driver
from mycaptcha import solve_captcha
from mysmtp import send_email
import time
import random
import datetime


global ID
global PW
ID = ["sunshower", "hl1xab", "hl0dil"]
PW = ["zaqxsw1599", "kb1211kb!", "kb1211kb!"]
SECTOR = ["001", "002", "003", "004"]

global updated_min
start_time = datetime.datetime.now()
updated_min = start_time.min

global switch_cnt
switch_cnt = random.randrange(0, 3)

web = Element()


def login():
    web.url("https://ticket.interpark.com/Gate/TPLogin.asp")
    web.iframe("first")
    web.find(id="userId").send_keys(ID[switch_cnt % 3])
    web.find(id="userPwd").send_keys(PW[switch_cnt % 3])
    web.find(id="btn_login").click()


def select_event():
    web.url("https://tickets.interpark.com/goods/24002990?app_tapbar_state=hide&")
    web.find(
        raw='//*[@id="productSide"]/div/div[1]/div[1]/div[2]/div/div/div/div/ul[3]/li[36]'
    ).click()
    web.find(text="예매하기").parent().click()


def pass_captcha():
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
    global switch_cnt
    global updated_min
    web.find(text="Floor 스탠딩").parent().click()

    while True:
        now = datetime.datetime.now()
        now_min = now.minute
        if updated_min != now_min and now_min == switch_min:
            switch_cnt += 1
            updated_min = now_min
            raise Exception()

        delayRefresh = random.uniform(1, 6)
        web.set_wait_until(timeout=delayRefresh, freq=0.01)

        web.iframe("default", "ifrmSeat")
        suddenCaptcha = web.uncertain(
            lambda: web.find(css_class="capchaLayer", style="display: block;")
        )
        if suddenCaptcha:
            pass_captcha()
        """Slider = web.uncertain(lambda: web.find(css_class="sliderContainer"))
        if Slider:
            print("fail")
            raise Exception()"""

        driver.execute_script(f"fnBlockSeatUpdate('', '', '{SECTOR[switch_cnt % 4]}')")
        web.iframe("ifrmSeatDetail")
        seat = web.uncertain(lambda: web.find(tag="span", name="Seats"))
        if seat:
            print("revealed")
            web.wait(0.4)
            seat.click()
            web.iframe("default", "ifrmSeat")
            web.wait(0.4)
            driver.execute_script("fnSelect();")

            send_email()
            web.wait(10000)


while True:
    plus_min = random.randrange(2, 21)
    now = datetime.datetime.now()
    switch_min = (now.minute + plus_min) % 60
    print(
        "switch_min:",
        f"{switch_min} = {now.minute} + {plus_min}",
        "\nID:",
        ID[switch_cnt % 3],
    )

    login()
    web.set_wait_until(timeout=5, freq=0.1)
    try:
        select_event()
        web.new_window()
        web.iframe("ifrmSeat")
        pass_captcha()
        select_seat()
    except Exception:
        web.wait(1)
        web.close()
        web.back_window()
        web.find(
            raw='//*[@id="ent-ticket__header"]/div[2]/div[1]/div/div[2]/a[1]'
        ).click()  # 로그아웃
        web.wait(1)
