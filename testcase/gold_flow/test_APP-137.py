from logic.deposit_page import deposit_revoke_or_audit_pass

import allure
import pytest


data = [{'username': 'welly229', 'pwd': 'qwer1234', 'deposit_method': 'offline'}]


@allure.feature('金流')
@allure.story('撤銷')
@pytest.mark.parametrize('driver_with_deposit_revoke_or_audit', data, indirect=True)
def test_revoke_deposit(driver_with_deposit_revoke_or_audit):
    case = 'revoke_deposit'

    username = data[0]['username']

    method = '线下入款'
    bank_name = '瑞士银行'
    deposit_name = 'haha'
    transfer_out_bank_name = '平安银行'
    remarks = '備註'
    amount = 100

    deposit_revoke_or_audit_pass(
        driver_with_deposit_revoke_or_audit,
        case,
        method,
        bank_name,
        username,
        deposit_name,
        transfer_out_bank_name,
        remarks,
        amount,
    )
