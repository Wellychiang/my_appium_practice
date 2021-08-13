from appium import webdriver
from common.base import log

import pytest


@pytest.fixture()
def driver():
    caps = {}
    caps["appActivity"] = "com.entertainment.mps_yabo.LandingActivity"
    caps["appPackage"] = "com.stage.mpsy.stg"
    caps["deviceName"] = "WUXDU19111001417"
    caps["platformName"] = "Android"
    caps["isHeadless"] = "true"

    log(f'Start app')
    driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
    yield driver
    driver.quit()
    log('Close app')

