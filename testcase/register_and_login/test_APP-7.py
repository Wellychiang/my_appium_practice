from page.login_page import LoginPage
from logic.login_page import failed_login

import allure
import pytest


@allure.feature('登入')
@allure.story('欄位填寫錯誤')
def test_failed_input(driver):
    """
    已註冊帳號: addcqdu58zvwn (這個會被封鎖, 到時候問下哪裡設定)
    未註冊帳號: addcqdu58zvwnasdsasss
    """
    account =   ('addcqdu58zvwn', 'addcqdu58zvwnasdsasss', 'qqq')
    pwd =       ('qqq', 'qqq', 'qwer1234')
    err_msg =   '账号或密码输入错误'

    login_page = LoginPage(driver)
    login_page.cancel_the_hint_with_new_version()
    login_page.skip_ad_page()

    [failed_login(
        username=account[i],
        pwd=pwd[i],
        err_msg=err_msg,
        login_page=login_page
    ) for i in range(3)]

