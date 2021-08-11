from appium import webdriver
from time import sleep
from page.login_page import LoginPage

import pytest
import allure


caps = {}
caps["appActivity"] = "com.entertainment.mps_yabo.LandingActivity"
caps["appPackage"] = "com.stage.mpsy.stg"
caps["deviceName"] = "WUXDU19111001417"
caps["platformName"] = "Android"


@pytest.fixture()
def driver():
    driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
    yield driver
    driver.quit()


@allure.feature('登入案例')
@allure.story('正常登入')
def test_login(driver):
    login_page = LoginPage(driver)
    login_page.skip_ad_page()
    login_page.input_username('autotest')
    login_page.input_pwd('1234qwer')
    login_page.click_login_button()

    # login_page.login(account='autotest', pwd='1234qwer')



if __name__ == '__main__':
    pytest.main(['-vvs', '--reruns', '1', '--alluredir', 'report'])

