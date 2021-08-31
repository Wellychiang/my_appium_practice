from page.home_page import HomePage
from page.deposit.deposit_page import DepositPage, OfflineDeposit
from page.deposit.deposit_success_page import DepositSuccessPage
from logic import deposit_page as logic

import allure
import pytest

data = [{'username': 'welly229', 'pwd': 'qwer1234'}]


@allure.feature('金流')
@allure.story('線下入款')
@pytest.mark.parametrize('driver', data, indirect=True)
def test_offline_deposit(driver):

    username = data[0]['username']

    bank_name = '瑞士银行'
    deposit_name = 'haha'
    transfer_out_bank_name = '平安银行'
    remarks = '備註'
    amount = 100


    home_page =             HomePage(driver)
    deposit_page =          DepositPage(driver)
    deposit_success_page =  DepositSuccessPage(driver)

    offline_deposit_ =           OfflineDeposit(driver)
    deposit_choose_amount_page = offline_deposit_.ChooseAmountPage(driver)


    deposit_page.choose_pay_method(method='线下入款')

    offline_deposit_.click_to_show_up_bank_list()
    offline_deposit_.click_to_choose_bank(bank_name=bank_name)

    offline_deposit_.check_bank_name_when_its_chosen(bank_name=bank_name)
    offline_deposit_.check_post_script(username=username)
    offline_deposit_.click_next_step()

    deposit_choose_amount_page.check_popup_warm_hint_and_click_confirm()
    deposit_choose_amount_page.input_name(deposit_name)
    deposit_choose_amount_page.click_to_show_up_transfer_out_bank_list()
    deposit_choose_amount_page.choose_transfer_out_bank(bank_name=transfer_out_bank_name)
    deposit_choose_amount_page.input_remark(remark=remarks)
    deposit_choose_amount_page.upload_img()

    deposit_choose_amount_page.check_immediately_deposit_is_enabled_or_not(bool_=True)
    deposit_choose_amount_page.choose_other_amount_button_then_input_amount(amount=amount)
    deposit_choose_amount_page.click_immediately_deposit()

    deposit_id = deposit_success_page.check_all_info_with_success_deposited(
        amount=amount,
        deposit_name=deposit_name,
        receive_payment_bank=bank_name,
        # transfer_out_bank=transfer_out_bank_name
    )
    deposit_success_page.click_close_and_go_back_to_home_page()

    home_page.check_bottom_navigator_display()

    logic.check_with_ims_deposit_audit_search(
        username,
        deposit_id,
        valid_amount=amount,
        remarks=remarks,
        deposit_name=deposit_name
    )


