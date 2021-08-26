from testcase import ims

import allure
import pytest


data = [{'username': 'welly229', 'pwd': 'qwer1234', 'deposit_method': 'Neteller'}]


@allure.feature('金流')
@allure.story('個人號轉帳-Neteller')
@pytest.mark.parametrize('driver', data, indirect=True)
def test_Neteller_deopsit(
        driver,
        deposit_method=data[0]['deposit_method'],
        deposit_name='haha',
        remark='備註',
        amount=100,
):
    (deposit_page,
     neteller_deposit) = driver

    deposit_page.choose_pay_method(method=deposit_method)

    neteller_deposit.choose_personal_num_transfer()
    neteller_deposit.choose_payment_channel()
    neteller_deposit.click_to_choose_bank(bank_name='Neteller')
    neteller_deposit.check_bank_name_when_its_chosen(bank_name='Neteller')
    neteller_deposit.input_name(name=deposit_name)
    neteller_deposit.input_remark(remark=remark)
    neteller_deposit.check_get_receive_payment_account_enabled_or_not(bool_=False)
    neteller_deposit.input_amount(amount)
    neteller_deposit.click_get_receive_payment_account(amount=amount)
