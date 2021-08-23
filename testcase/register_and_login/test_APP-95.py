import allure
import pytest


@allure.feature('登入')
@allure.story('欄位填寫空值')
def test_empty_input(driver):
    login_page = driver[0]
    login_page.skip_ad_page()

    # 已註冊帳號
    login_page.input_username(account='addaur1180v23')
    login_page.input_pwd(pwd='')
    login_page.click_login_button()
    login_page.check_error_msg(err_msg='请输入密码')

    # 未註冊帳號
    login_page.input_username(account='asddddqqqwwwwe111234q')
    login_page.input_pwd(pwd='')
    login_page.close_keyboard()
    login_page.click_login_button()
    login_page.check_error_msg(err_msg='请输入密码')

    login_page.input_username(account='')
    login_page.input_pwd(pwd='')
    login_page.close_keyboard()
    login_page.click_login_button()
    login_page.check_error_msg(err_msg='请输入账号')

    login_page.input_username(account='')
    login_page.input_pwd(pwd='qqqqqq')
    login_page.close_keyboard()
    login_page.click_login_button()
    login_page.check_error_msg(err_msg='请输入账号')

