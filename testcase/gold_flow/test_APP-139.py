from testcase import ims

import allure
import pytest


@allure.feature('金流')
@allure.story('網銀轉帳')
def test_net_bank_deposit(
        driver,
        username='welly229',
        pwd='qwer1234',
        bank_name='瑞士银行',
        tranfer_out_bank_name=''

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

    deposit_method_choose.choose_pay_method(method='网银转账')
    deposit_receive_payment_bank.click_to_show_up_bank_list()
    deposit_receive_payment_bank.click_to_choose_bank(bank_name=bank_name)

    deposit_bank_detail.check_bank_name_when_its_chosen(bank_name=bank_name)
    deposit_bank_detail.check_post_script(username=username)
    deposit_bank_detail.click_next_step()




