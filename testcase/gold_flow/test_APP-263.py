from logic import deposit_page as logic
from page.home_page import HomePage
from page.deposit.deposit_page import DepositPage
from page.deposit.transfer_check_page import TransferCheckPage
from page.deposit.deposit_success_page import DepositSuccessPage

import allure
import pytest


data = [{'username': 'welly229', 'pwd': 'qwer1234'}]


@allure.feature('金流')
@allure.story('個人號轉賬-Neteller')
@pytest.mark.parametrize('driver', data, indirect=True)
def test_Neteller_deposit(driver):

    home_page =             HomePage(driver)
    deposit_page =          DepositPage(driver)
    deposit_success_page =  DepositSuccessPage(driver)
    transfer_check_page =   TransferCheckPage(driver)

    username =  'welly229'

    deposit_method =    'Neteller'
    bank_name =         '自動化'
    deposit_name =      'haha'
    remark =            '備註'
    invalid_amount =    (99, 10001)
    valid_amount =      100



    deposit_page.choose_pay_method(method=deposit_method)

    deposit_page.choose_personal_num_transfer()
    deposit_page.choose_payment_channel()
    deposit_page.click_to_choose_bank(bank_name=bank_name)
    deposit_page.check_bank_name_when_its_chosen(bank_name=bank_name)

    logic.input_and_check_rules_with_name_remark_and_amount(
        driver,
        deposit_name,
        remarks=remark,
        valid_amount=valid_amount,
        invalid_amount=invalid_amount
    )

    deposit_page.click_get_receive_payment_account()

    transfer_check_page.check_input_info_before_transfer(
        transfer_method=deposit_method,
        deposit_name=deposit_name,
        deposit_amount=valid_amount,
        name=username
    )
    # transfer_check_page.check_copy_function()
    logic.upload_image(driver)
    transfer_check_page.click_transfer_success()

    deposit_id = deposit_success_page.check_all_info_with_success_deposited(
        amount=valid_amount,
        deposit_name=deposit_name,
        receive_payment_bank=bank_name,
    )

    deposit_success_page.click_close_and_go_back_to_home_page()

    home_page.check_bottom_navigator_display()

    logic.check_with_ims_deposit_audit_search(
        username,
        deposit_id,
        valid_amount=valid_amount,
        remarks=None,
        deposit_name=deposit_name
    )
