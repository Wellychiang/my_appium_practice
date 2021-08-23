from appium import webdriver
from common.base import log

from page.login_page import LoginPage
from page.home_page import HomePage
from page.deposit_page import DepositPage
from page.deposit_record_page import DepositRecordPage

import pytest


@pytest.fixture()
def driver():
    caps = {
        "appActivity": "com.entertainment.mps_yabo.LandingActivity",
        "appPackage": "com.stage.mpsy.stg",
        "deviceName": "WUXDU19111001417",
        "platformName": "Android",
        "isHeadless": "true",
    }

    log(f'\n{"*"*8}Start app{"*"*8}')
    driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)

    login_page =            LoginPage(driver)
    home_page =             HomePage(driver)
    deposit_page =          DepositPage(driver)
    deposit_record_page =   DepositRecordPage(driver)

    home_bottom_navigator_bar =     home_page.BottomNavigatorBar(driver)
    deposit_method_choose =         deposit_page.MethodChoose(driver)
    deposit_receive_payment_bank =  deposit_page.ReceivePaymentBank(driver)
    deposit_bank_detail =           deposit_page.BankDetail(driver)
    deposit_choose_amount_page =    deposit_page.ChooseAmountPage(driver)
    deposit_success_page =          deposit_page.DepositSuccessPage(driver)

    yield (
        login_page,
        home_page,
        deposit_page,
        deposit_record_page,
        home_bottom_navigator_bar,
        deposit_method_choose,
        deposit_receive_payment_bank,
        deposit_bank_detail,
        deposit_choose_amount_page,
        deposit_success_page
    )
    driver.quit()
    log(f'{"*"*8}Close app{"*"*8}')

