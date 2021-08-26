from logic.login_page import login

import allure
import pytest


@allure.feature('登入')
@allure.story('正常登入')
def test_login(driver):
    username = 'welly'
    pwd = 'qwer1234'

    login(driver, username, pwd)

