# from logic.login_page import login

from page.login_page import LoginPage

import allure
import pytest


@allure.feature('登入')
@allure.story('正常登入')
def test_login(driver):
    username = 'welly'
    pwd = 'qwer1234'

    # login(driver, username, pwd)

    login_page = LoginPage(driver)

    login_page.cancel_the_hint_with_new_version()
    login_page.skip_ad_page()
    login_page.input_username(username)
    login_page.input_pwd(pwd)
    login_page.click_login_button()
