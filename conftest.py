from appium import webdriver
from common.base import log

from page.login_page import LoginPage
from page.home_page import HomePage
from page.deposit_page import DepositPage
from page.deposit_page import OfflineDeposit
from page.deposit_page import NetbankDeposit
from page.deposit_record_page import DepositRecordPage

import pytest


@pytest.fixture()
def driver():
    caps = {
        "appActivity": "com.entertainment.mps_yabo.LandingActivity",
        "appPackage": "com.stage.mpsy.stg",
        "deviceName": "WUXDU19111001417",
        "platformName": "Android",
        "automationName": "uiautomator2",
        "isHeadless": "true",
    }

    log(f'\n{"*"*8}Start app{"*"*8}')
    driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)

    login_page =                    LoginPage(driver)
    home_page =                     HomePage(driver)
    deposit_page =                  DepositPage(driver)
    deposit_record_page =           DepositRecordPage(driver)

    home_bottom_navigator_bar =     home_page.BottomNavigatorBar(driver)
    offline_deposit =               OfflineDeposit(driver)
    deposit_choose_amount_page =    OfflineDeposit(driver).ChooseAmountPage(driver)
    deposit_success_page =          OfflineDeposit(driver).DepositSuccessPage(driver)

    netbank_deposit =               NetbankDeposit(driver)

    yield (
        login_page,
        home_page,
        home_bottom_navigator_bar,
        deposit_page,
        deposit_record_page,
        offline_deposit,
        deposit_choose_amount_page,
        deposit_success_page,

        netbank_deposit,
    )
    driver.quit()
    log(f'{"*"*8}Close app{"*"*8}')

