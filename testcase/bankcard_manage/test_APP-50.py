from page.account.account_page import AccountPage
from page.account.bankcard_manage_page import BankcardManagePage
from page.account.add_bankcard_page import AddBankcardPage

from logic import bankcard_manage_page as bankcard
import allure
import pytest
import random
import time

data = [{'username': 'welly229', 'pwd': 'qwer1234'}]


@allure.feature('銀行卡管理')
@allure.story('添加銀行卡')
@pytest.mark.parametrize('driver', data, indirect=True)
def test_add_bankcard(driver):
    """
    這用例只有 happy path, 之後要補上規則判斷
    """
    bankcard_manage_page =  BankcardManagePage(driver)

    bank_name =         '平安银行'
    bankcard_status =   '激活'

    bank_account, init_bankcard_count = bankcard.add_bankcard(driver, bank_name=bank_name)

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

