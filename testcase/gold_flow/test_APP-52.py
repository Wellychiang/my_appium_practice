from testcase import ims

import allure
import pytest


@allure.feature('金流')
@allure.story('線下入款')
def test_offline_deposit(
        driver,
        username='welly229',
        pwd='qwer1234',
        bank_name='瑞士银行',
        transfer_out_bank_name='平安银行',
        deposit_name='haha',
        amount=100,
        remarks='備註',
):
    (login_page,
     home_page,
     deposit_page,
     deposit_record_page,
     home_bottom_navigator_bar,
     deposit_method_choose,
     deposit_receive_payment_bank,
     deposit_bank_detail,
     deposit_choose_amount_page,
     deposit_success_page) = driver

    ims.set_up_payment_settings()

    login_page.login(account=username, pwd=pwd)

    home_page.ignore_gift_if_it_show_up()
    # TODO: 每日簽到的 skip
    home_page.ignore_ads_if_ads_show_up()
    home_page.click_deposit_button()
    deposited = home_page.go_revoke_deposit_page_if_deposited()
    if deposited is True:
        deposit_record_page.revoke_deposit()
        home_page.click_deposit_button()

    deposit_method_choose.choose_pay_method(method='线下入款')
    deposit_receive_payment_bank.click_to_show_up_bank_list()
    deposit_receive_payment_bank.click_to_choose_bank(bank_name=bank_name)

    deposit_bank_detail.check_bank_name_when_its_chosen(bank_name=bank_name)
    deposit_bank_detail.check_post_script(username=username)
    deposit_bank_detail.click_next_step()

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
        transfer_out_bank=transfer_out_bank_name
    )
    deposit_success_page.click_close_and_go_back_to_home_page()

    home_bottom_navigator_bar.check_bottom_navigator_display()

    deposit_audit_search = ims.deposit_audit_search(playerid=username)
    assert deposit_audit_search['total'] == 1
    assert deposit_audit_search['data'][0]['depositid'] == deposit_id
    assert deposit_audit_search['data'][0]['caccountbankname'] == bank_name
    assert deposit_audit_search['data'][0]['depositamt'] == amount
    assert deposit_audit_search['data'][0]['receiveddepositamt'] == amount
    assert deposit_audit_search['data'][0]['playerid'] == username
    assert deposit_audit_search['data'][0]['remarks'] == remarks
    assert deposit_audit_search['data'][0]['depositname'] == deposit_name
