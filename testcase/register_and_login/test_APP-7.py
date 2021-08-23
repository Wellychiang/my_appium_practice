
import allure
import pytest


@allure.feature('登入')
@allure.story('欄位填寫錯誤')
def test_failed_input(driver):
    login_page = driver[0]
    login_page.skip_ad_page()

    # 已註冊帳號
    login_page.input_username(account='addcqdu58zvwn')
    login_page.input_pwd(pwd='qqq')
    login_page.close_keyboard()
    login_page.click_login_button()
    login_page.check_error_msg(err_msg='账号或密码输入错误')

    # 未註冊帳號
    login_page.input_username(account='addcqdu58zvwnasdsasss')
    login_page.input_pwd(pwd='qqq')
    login_page.close_keyboard()
    login_page.click_login_button()
    login_page.check_error_msg(err_msg='账号或密码输入错误')

    login_page.input_username(account='qqq')
    login_page.input_pwd(pwd='qwer1234')
    login_page.close_keyboard()
    login_page.click_login_button()
    login_page.close_keyboard()
    login_page.check_error_msg(err_msg='账号或密码输入错误')
