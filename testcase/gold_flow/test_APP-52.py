from logic.deposit_page import offline_deposit
from logic.login_page import login

import allure
import pytest


@allure.feature('金流')
@allure.story('線下入款')
def test_offline_deposit(driver):
    username = 'welly220'
    pwd = 'qwer1234'
    bank_name = '瑞士银行',
    username = username,
    transfer_out_bank_name = '平安银行',
    deposit_name = 'haha',
    amount = 100,
    remarks = '備註',

    login(driver, username, pwd)
    offline_deposit(
        driver,
        bank_name,
        username,
        transfer_out_bank_name,
        deposit_name,
        amount,
        remarks,
    )


