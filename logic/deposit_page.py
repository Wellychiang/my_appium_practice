from page.deposit.deposit_page import DepositPage
from page.deposit.deposit_page import OfflineDeposit
from page.deposit.deposit_success_page import DepositSuccessPage
from page.deposit.transfer_check_page import TransferCheckPage
from page.deposit_record_page import DepositRecordPage
from page.home_page import HomePage
from page.account.account_page import AccountPage
from page.account.finance_record_page import FinanceRecordPage
from common.base import Ims

import allure
import pytest




def deposit_revoke_or_audit_pass(
        driver,
        case,
        method,
        bank_name,
        username,
        deposit_name,
        transfer_out_bank_name,
        remarks,
        amount,
):
    ims = Ims()

    home_page =             HomePage(driver)
    deposit_page =          DepositPage(driver)
    deposit_success_page =  DepositSuccessPage(driver)
    deposit_record_page =   DepositRecordPage(driver)

    offline_deposit_ =           OfflineDeposit(driver)
    deposit_choose_amount_page = offline_deposit_.ChooseAmountPage(driver)

    account_page =      AccountPage(driver)
    finance_record_page =    FinanceRecordPage(driver)


    deposit_page.choose_pay_method(method=method)

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
    )
    deposit_success_page.click_close_and_go_back_to_home_page()

    home_page.check_bottom_navigator_display()

    deposit_audit_search = check_with_ims_deposit_audit_search(
        username,
        deposit_id,
        valid_amount=amount,
        remarks=remarks,
        deposit_name=deposit_name
    )

    if case == 'revoke_deposit':
        home_page.click_deposit_button()
        home_page.click_close_if_deposit_hint_displayed()
        home_page.click_deposit_button()
        home_page.go_revoke_deposit_page_if_deposited()
        deposit_record_page.revoke_deposit()

        deposit_audit_search = ims.deposit_audit_search(playerid=username)
        assert deposit_audit_search['total'] == 0
        assert len(deposit_audit_search['data']) == 0
    elif case == 'audit_pass':
        ec_remarks = 'empleee'

        deposit_id = deposit_audit_search['data'][0]['depositid']
        unlock_status = ims.deposit_data_lock_or_not(deposit_id=deposit_id, status='unlock')
        approve_status = ims.deposit_data_approve(deposit_id=deposit_id, ec_remarks=ec_remarks)
        if str(unlock_status) != '204' or str(approve_status) != '204':
            raise ValueError(f'IMS unlock status: {unlock_status}\tIMS approve status: {approve_status}')

        home_page.go_to_account()

        account_page.go_to_finance_record()
        finance_record_page.check_deposit_info(count=1, title='存款', status='成功', amount=amount)
        # transaction_detail.check_amount(amount=amount)
        # transaction_detail.check_status(status=status)
        # transaction_detail.check_remark(remark=ec_remarks)


def personal_account_transfer(
        driver,
        username,
        deposit_method,
        bank_name,
        deposit_name,
        remark,
        valid_amount,
        invalid_amount: tuple

):
    ims = Ims()

    home_page =             HomePage(driver)
    deposit_record_page =   DepositRecordPage(driver)
    deposit_page =          DepositPage(driver)
    deposit_success_page =  DepositSuccessPage(driver)

    deposit_page = TransferCheckPage(driver)


    deposit_page.choose_pay_method(method=deposit_method)

    deposit_page.choose_personal_num_transfer()
    deposit_page.choose_payment_channel()
    deposit_page.click_to_choose_bank(bank_name=bank_name)
    deposit_page.check_bank_name_when_its_chosen(bank_name=bank_name)

    input_and_check_rules_with_name_remark_and_amount(
        driver,
        deposit_name,
        remarks=remark,
        valid_amount=valid_amount,
        invalid_amount=invalid_amount
    )

    deposit_page.click_get_receive_payment_account()

    deposit_page.check_input_info_before_transfer(
        transfer_method=deposit_method,
        deposit_name=deposit_name,
        deposit_amount=valid_amount,
        name=username
    )
    # deposit_page.check_copy_function()
    upload_image(driver)
    # deposit_page.upload_img()
    deposit_page.click_transfer_success()

    deposit_id = deposit_success_page.check_all_info_with_success_deposited(
        amount=valid_amount,
        deposit_name=deposit_name,
        receive_payment_bank=bank_name,
    )

    deposit_success_page.click_close_and_go_back_to_home_page()

    home_page.check_bottom_navigator_display()

    check_with_ims_deposit_audit_search(
        username,
        deposit_id,
        valid_amount=valid_amount,
        remarks=None,
        deposit_name=deposit_name
    )



def input_and_check_rules_with_name_remark_and_amount(
        driver,
        deposit_name:   str,
        remarks:        str,
        valid_amount:   int,
        invalid_amount: tuple
):
    deposit_page = DepositPage(driver)

    deposit_page.input_name(name=deposit_name)
    deposit_page.check_get_receive_payment_account_enabled_or_not(bool_=False)
    deposit_page.input_remark(remark=remarks)
    deposit_page.check_get_receive_payment_account_enabled_or_not(bool_=True)

    deposit_page.click_another_amount()
    # TODO: 等 android 版本修復: 點擊其他金額時, 未輸入卻可以送出(按鈕未顯示灰色)
    # deposit_page.check_get_receive_payment_account_enabled_or_not(bool_=False)
    deposit_page.input_amount(amount=valid_amount)
    deposit_page.find_element(deposit_page.amount_placeholder).clear()
    deposit_page.check_red_hint_with_invalid_input(err_msg="请输入充值金额")
    # deposit_page.check_get_receive_payment_account_enabled_or_not(bool_=False)
    deposit_page.input_amount(amount=invalid_amount[0])
    deposit_page.check_red_hint_with_invalid_input(err_msg="充值限额100.00 - 10,000.00 CNY")
    deposit_page.check_get_receive_payment_account_enabled_or_not(bool_=False)
    deposit_page.input_amount(amount=invalid_amount[1])
    deposit_page.check_red_hint_with_invalid_input(err_msg="充值限额100.00 - 10,000.00 CNY")
    deposit_page.check_get_receive_payment_account_enabled_or_not(bool_=False)
    deposit_page.input_amount(amount=valid_amount)


def check_with_ims_deposit_audit_search(
        username,
        deposit_id,
        valid_amount,
        remarks,
        deposit_name
):
    ims = Ims()

    deposit_audit_search = ims.deposit_audit_search(playerid=username)
    assert deposit_audit_search['total'] == 1
    assert deposit_audit_search['data'][0]['depositid'] == deposit_id
    assert deposit_audit_search['data'][0]['depositamt'] == valid_amount
    assert deposit_audit_search['data'][0]['receiveddepositamt'] == valid_amount
    assert deposit_audit_search['data'][0]['playerid'] == username
    assert deposit_audit_search['data'][0]['remarks'] == remarks
    assert deposit_audit_search['data'][0]['depositname'] == deposit_name

    return deposit_audit_search


def upload_image(driver):
    deposit_page = DepositPage(driver)

    deposit_page.click_image_btn()
    deposit_page.click_from_picture_lib()
    deposit_page.allowed_app_load_image()

    deposit_page.click_image_btn()
    deposit_page.click_from_picture_lib()
    deposit_page.choose_the_first_in_lib()
    deposit_page.upload_the_chosen_image()
