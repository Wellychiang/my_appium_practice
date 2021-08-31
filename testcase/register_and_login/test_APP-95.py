from page.login_page import LoginPage
from logic.login_page import failed_login

import allure
import pytest


@allure.feature('登入')
@allure.story('欄位填寫空值')
def test_empty_input(driver):
    """
    已註冊帳號: addaur1180v23
    未註冊帳號: asddddqqqwwwwe111234q
    """
    account =   ('addaur1180v23', 'asddddqqqwwwwe111234q', '', '')
    pwd =       ('', '', '', 'qqqq')
    err_msg =   ('请输入密码', '请输入密码', '请输入账号', '请输入账号')

    login_page = LoginPage(driver)
    login_page.cancel_the_hint_with_new_version()
    login_page.skip_ad_page()

    [failed_login(
        username=account[i],
        pwd=pwd[i],
        err_msg=err_msg[i],
        login_page=login_page,
    ) for i in range(4)]
