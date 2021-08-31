from page.account.account_page import AccountPage
from page.account.bankcard_manage_page import BankcardManagePage
from page.account.add_bankcard_page import AddBankcardPage
from page.account.bankcard_info import BankcardInfo

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
    add_bankcard_page = AddBankcardPage(driver)
    bankcard_info = BankcardInfo(driver)

    random_key = '12345678901239872350293' + str(time.time())[-6:-1]

    bank_name = '平安银行'
    bank_account = ''.join(random.sample(random_key, 22))
    bankcard_status = '激活'

    account_page.go_to_bankcard_manage()

    init_bankcard_count = bankcard_manage_page.return_how_many_bankcard_now()
    if int(init_bankcard_count) >= 4:
        bankcard_manage_page.slide('swipe up')
    bankcard_manage_page.click_add_bankcard()

    add_bankcard_page.click_to_show_up_bank_list()
    add_bankcard_page.choose_bank(bank_name=bank_name)
    add_bankcard_page.input_bank_account(bank_account=bank_account)
    add_bankcard_page.click_confirm_btn()
    add_bankcard_page.check_add_bankcard_success_msg()

    card_after_added = init_bankcard_count + 1
    if card_after_added >= 4:
        bankcard_manage_page.slide('swipe up')

    bankcard_manage_page.check_bankcard_account(
        bank_account=bank_account,
        count=card_after_added
    )
    bankcard_manage_page.check_bankcard_bank(
        bank_name=bank_name,
        count=card_after_added
    )

    bankcard_manage_page.check_bankcard_status(
        status=bankcard_status,
        count=card_after_added
    )

    bankcard_manage_page.click_bankcard_to_my_bankcard_page(bank_account=bank_account)

    bankcard_info.input_pwd(pwd=data[0]['pwd'])
    bankcard_info.click_confirm_to_update_my_bankcard_info()
    bankcard_info.check_edit_bankcard_success_hint()
