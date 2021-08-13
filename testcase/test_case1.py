from . import import_all_pages_driver, LoginPage

import allure



@allure.feature('登入案例')
@allure.story('正常登入')
def test_login(driver):
    login_page = LoginPage(driver)
    login_page.skip_ad_page()
    login_page.input_username('autotest')
    login_page.input_pwd('1234qwer')
    login_page.click_login_button()


@allure.feature('轉帳測試')
@allure.story('正常登入')
def test_tt(driver):
    login_page, home_page, deposit_page = import_all_pages_driver(driver)

    login_page.login(account='autotest', pwd='1234qwer')

    home_page.ignore_ads_if_ads_show_up()
    home_page.click_deposit_button()

    deposit_page.choose_offline_button()
    deposit_page.click_to_show_up_bank_list()
    deposit_page.click_to_choose_bank(bank_name='成都')
    deposit_page.display_buttom_sheet_or_not(bool_=False)
    deposit_page.check_bank_name_when_its_chosen(bank_name='成都')
    deposit_page.check_subbank_name_when_its_chosen(subbank_name='上海')





