from testcase import ims

import allure
import pytest


data = [{'username': 'welly229', 'pwd': 'qwer1234', 'deposit_method': 'netbank'}]


@allure.feature('金流')
@allure.story('網銀轉帳')
@pytest.mark.parametrize("driver", data, indirect=True)
def test_net_bank_deposit(
        driver,
        username=data[0]['username'],
        transfer_out_bank_name='平安银行',
        receive_payment_bank_name='瑞士银行',
        remarks='備註',
        amount=100,
):
    (deposit_page,
     netbank_deposit) = driver

    deposit_page.choose_pay_method(method='网银转账')
    netbank_deposit.click_to_show_up_transfer_out_bank_list()
    netbank_deposit.choose_transfer_out_bank(bank_name=transfer_out_bank_name)
    netbank_deposit.check_bank_name_when_its_chosen(bank_name=transfer_out_bank_name)

    netbank_deposit.click_to_show_up_receive_payment_bank_list()
    netbank_deposit.click_to_choose_bank(bank_name=receive_payment_bank_name)
    netbank_deposit.check_bank_name_when_its_chosen(bank_name=receive_payment_bank_name)

    # netbank_deposit.input_name(name=username)
    # netbank_deposit.input_remark(remark=remarks)

    # netbank_deposit.choose_other_amount_button_then_input_amount(amount=amount)
    # TODO: 等 android 版本修復: 點擊其他金額時, 未輸入卻可以送出(按鈕未顯示灰色)

