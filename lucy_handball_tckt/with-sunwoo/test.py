from driver import Element, driver
import time

ID = "hl2dil"
PW = "kb1211kb!"

web = Element()

web.set_wait_until(timeout=10, freq=0.1)

web.url("https://ticket.interpark.com/Gate/TPLogin.asp")
web.iframe("first")
web.find(id="userId").send_keys(ID)
web.find(id="userPwd").send_keys(PW)
web.find(id="btn_login").click()

while True:
    web.url("https://tickets.interpark.com/goods/24001548")
    web.find(text="예매하기").parent().click()

    web.new_window()
    web.iframe("ifrmSeat")
    web.find(text="VIP석").parent().click()
    web.set_wait_until(timeout=0.05, freq=0.01)
    # web.find(tag="li", text_c="석", text_n=" (0석)").find(tag="a").click()
    isBreak = False
    while True:
        web.iframe("default", "ifrmSeat")
        driver.execute_script("fnBlockSeatUpdate('', '', '003')")
        print("refresh")
        web.iframe("ifrmSeatDetail")
        starttime = time.time()
        seat = web.uncertain(lambda: web.find_all(tag="span", name="Seats")[:4][0])
        print(time.time() - starttime)
        if seat:
            seat.click()
            web.iframe("default", "ifrmSeat")
            driver.execute_script("fnSelect();")
            isBreak = True
            break

    if isBreak:
        break

    web.close()


# smtp 쓰기
