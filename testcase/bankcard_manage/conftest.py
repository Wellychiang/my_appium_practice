from appium import webdriver
from common.base import log
from common.base import Ims

from page.login_page import LoginPage
from page.home_page import HomePage



from testcase import ims

import pytest
import allure


@allure.step('初始化充值頁面, 已充值帳號')
def setup_settings(playerid):

    log(f'\n{"-"*8}Setup settings{"-"*8}')

    ims = Ims()
    bankcard_datas = ims.bankcard(playerid)
    for data in bankcard_datas['data']:
        ims.bankcard(playerid, delete=True, payment_id=data['paymentid'])

    log(f'\n{"-"*8}Settings done{"-"*8}')


@pytest.fixture()
def driver(request):
    log(f'\n{"-"*8}Start app{"-"*8}')
    param = request.param
    setup_settings(playerid=param['username'])
    caps = {
        "appActivity": "com.entertainment.mps_yabo.LandingActivity",
        "appPackage": "com.stage.mpsy.stg",
        "deviceName": "WUXDU19111001417",
        "platformName": "Android",
        "automationName": "uiautomator2",
        "isHeadless": "true",
    }
    driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)

    login_page =                    LoginPage(driver)
    home_page =                     HomePage(driver)

    try:
        login_page.login(account=param['username'], pwd=param['pwd'])

        home_page.ignore_gift_if_it_show_up()
        # TODO: 每日簽到的 skip
        home_page.ignore_ads_if_ads_show_up()
        home_page.go_to_account()

        yield driver

    except Exception as e:
        raise ValueError(str(e))
    finally:
        driver.quit()


