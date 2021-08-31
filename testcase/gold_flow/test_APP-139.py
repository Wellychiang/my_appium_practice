from logic import deposit_page as logic
from page.home_page import HomePage
from page.deposit.deposit_page import NetbankDeposit
from page.deposit.transfer_check_page import TransferCheckPage
from page.deposit.deposit_success_page import DepositSuccessPage


import allure
import pytest


data = [{'username': 'welly229', 'pwd': 'qwer1234'}]


@allure.feature('金流')
@allure.story('網銀轉帳')
@pytest.mark.parametrize("driver", data, indirect=True)
def test_net_bank_deposit(driver):

    home_page = HomePage(driver)
    netbank_deposit =       NetbankDeposit(driver)
    deposit_success_page = DepositSuccessPage(driver)
    transfer_check_page = TransferCheckPage(driver)

    username = data[0]['username']

    deposit_method = '网银转账'
    transfer_out_bank_name = '平安银行'
    receive_payment_bank_name = '瑞士银行'
    remarks = '備註'
    deposit_name = 'qq'
    valid_amount = 100
    invalid_amount = (99, 10001)


    netbank_deposit.choose_pay_method(deposit_method)
    netbank_deposit.click_to_show_up_transfer_out_bank_list()

    netbank_deposit.choose_transfer_out_bank(bank_name=transfer_out_bank_name)
    netbank_deposit.check_bank_name_when_its_chosen(bank_name=transfer_out_bank_name)

    netbank_deposit.click_to_show_up_receive_payment_bank_list()
    netbank_deposit.click_to_choose_bank(bank_name=receive_payment_bank_name)
    netbank_deposit.check_bank_name_when_its_chosen(bank_name=receive_payment_bank_name)

    logic.input_and_check_rules_with_name_remark_and_amount(
        driver,
        deposit_name,
        remarks=remarks,
        valid_amount=valid_amount,
        invalid_amount=invalid_amount
    )
    netbank_deposit.click_get_receive_payment_account()

    transfer_check_page .check_input_info_before_transfer(
        transfer_method=deposit_method,
        deposit_name=deposit_name,
        deposit_amount=valid_amount,
        name=username
    )
    # TODO: 複製 appium 找不到, 先略過
    # deposit_page.check_copy_function()
    logic.upload_image(driver)
    transfer_check_page.click_transfer_success()

    deposit_id = deposit_success_page.check_all_info_with_success_deposited(
        amount=valid_amount,
        deposit_name=deposit_name,
        receive_payment_bank=receive_payment_bank_name,
    )

    deposit_success_page.click_close_and_go_back_to_home_page()

    home_page.check_bottom_navigator_display()

    logic.check_with_ims_deposit_audit_search(
        username,
        deposit_id,
        valid_amount,
        remarks,
        deposit_name
    )

