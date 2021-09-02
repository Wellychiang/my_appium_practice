from page.account.account_page import AccountPage
from page.account.bankcard_manage_page import BankcardManagePage
from page.account.add_bankcard_page import AddBankcardPage
from page.account.bankcard_info import BankcardInfo

from logic import bankcard_manage_page as bankcard

import allure
import pytest
import random
import time

data = [{'username': 'welly229', 'pwd': 'qwer1234'}]


@allure.feature('銀行卡管理')
@allure.story('編輯銀行卡')
@pytest.mark.parametrize('driver', data, indirect=True)
def test_edit_bankcard(driver):
    """一樣 happy path, 判斷再補上"""
    account_page = AccountPage(driver)
    bankcard_manage_page = BankcardManagePage(driver)
    bankcard_info = BankcardInfo(driver)

    bank_name = '平安银行'

    bank_account, init_bankcard_count = bankcard.add_bankcard(driver, bank_name=bank_name)

    card_after_added = init_bankcard_count + 1
    if card_after_added >= 4:
        bankcard_manage_page.slide('swipe up')

    bankcard_manage_page.click_bankcard_to_my_bankcard_page(bank_account=bank_account)

    bankcard_info.input_pwd(pwd=data[0]['pwd'])
    bankcard_info.click_confirm_to_update_my_bankcard_info()
    bankcard_info.check_edit_bankcard_success_hint()
