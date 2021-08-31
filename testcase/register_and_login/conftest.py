from appium import webdriver
from common.base import log

from page.login_page import LoginPage
from page.home_page import HomePage
from page.deposit.deposit_page import DepositPage, OfflineDeposit, NetbankDeposit
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

    yield driver

    driver.quit()
    log(f'{"*"*8}Close app{"*"*8}')

