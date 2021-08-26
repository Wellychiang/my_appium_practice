
import allure
import pytest


@allure.feature('登入')
@allure.story('正常登入')
def test_login(driver):
    login_page = driver[0]
    bottom_nav = driver[2]

    login_page.skip_ad_page()
    login_page.input_username('welly229')
    login_page.input_pwd('qwer1234')
    login_page.click_login_button()

    bottom_nav.check_bottom_navigator_display()

