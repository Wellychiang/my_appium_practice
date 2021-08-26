from appium import webdriver
from common.base import log

from page.login_page import LoginPage
from page.home_page import HomePage
from page.account_page import AccountPage
from page.deposit_page import DepositPage
from page.deposit_page import OfflineDeposit
from page.deposit_page import NetbankDeposit
from page.deposit_page import NetellerDeposit
from page.deposit_record_page import DepositRecordPage

from testcase import ims

import os
import pytest


@pytest.fixture()
def driver(request):
    log(f'\n{"*"*8}Start app{"*"*8}')

    param = request.param
    ims.set_up_deposit_page_settings(deposit_method=param['deposit_method'])
    caps = {
        "appActivity": "com.entertainment.mps_yabo.LandingActivity",
        "appPackage": "com.stage.mpsy.stg",
        "deviceName": "WUXDU19111001417",
        "platformName": "Android",
        "automationName": "uiautomator2",
        "isHeadless": "true",
    }
    driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)

    login_page =                    LoginPage(driver)
    home_page =                     HomePage(driver)
    deposit_page =                  DepositPage(driver)
    deposit_record_page =           DepositRecordPage(driver)

    home_bottom_navigator_bar =     home_page.BottomNavigatorBar(driver)
    offline_deposit =               OfflineDeposit(driver)
    deposit_choose_amount_page =    OfflineDeposit(driver).ChooseAmountPage(driver)
    deposit_success_page =          OfflineDeposit(driver).DepositSuccessPage(driver)

    netbank_deposit =               NetbankDeposit(driver)
    neteller_deposit =              NetellerDeposit(driver)


    login_page.login(account=param['username'], pwd=param['pwd'])

    home_page.ignore_gift_if_it_show_up()
    # TODO: 每日簽到的 skip
    home_page.ignore_ads_if_ads_show_up()
    home_page.click_deposit_button()
    deposited = home_page.go_revoke_deposit_page_if_deposited()
    if deposited is True:
        deposit_record_page.revoke_deposit()

    init_methods = []
    if param['deposit_method'] == 'offline':
        init_methods.extend([
            home_bottom_navigator_bar,
            deposit_page,
            offline_deposit,
            deposit_choose_amount_page,
            deposit_success_page
        ])
    elif param['deposit_method'] == 'Neteller':
        init_methods.extend([
            deposit_page,
            neteller_deposit
        ])
    elif param['deposit_method'] == 'netbank':
        init_methods.extend([deposit_page, netbank_deposit])
    else:
        pass

    yield init_methods

    home_page.click_deposit_button()
    deposited = home_page.go_revoke_deposit_page_if_deposited()
    if deposited is True:
        deposit_record_page.revoke_deposit()

    driver.quit()
    log(f'{"*"*8}Close app{"*"*8}')


@pytest.fixture()
def driver_with_audit_related(request):
    """ for test_APP-137, 138"""

    log(f'\n{"*" * 8}Start app{"*" * 8}')

    param = request.param
    ims.set_up_deposit_page_settings(deposit_method=param['deposit_method'])
    caps = {
        "appActivity": "com.entertainment.mps_yabo.LandingActivity",
        "appPackage": "com.stage.mpsy.stg",
        "deviceName": "WUXDU19111001417",
        "platformName": "Android",
        "automationName": "uiautomator2",
        "isHeadless": "true",
    }
    driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)

    login_page =                 LoginPage(driver)
    home_page =                  HomePage(driver)
    home_bottom_navigator_bar =  home_page.BottomNavigatorBar(driver)

    deposit_page =                  DepositPage(driver)
    offline_deposit =               OfflineDeposit(driver)
    netbank_deposit =               NetbankDeposit(driver)
    deposit_choose_amount_page =    OfflineDeposit(driver).ChooseAmountPage(driver)
    deposit_success_page =          OfflineDeposit(driver).DepositSuccessPage(driver)
    deposit_record_page =           DepositRecordPage(driver)

    account_page =       AccountPage(driver)
    finance_record =     account_page.FinanceRecord(driver)
    transaction_detail = finance_record.TransactionDetail(driver)


    login_page.login(account=param['username'], pwd=param['pwd'])

    home_page.ignore_gift_if_it_show_up()
    # TODO: 每日簽到的 skip
    home_page.ignore_ads_if_ads_show_up()
    home_page.click_deposit_button()
    deposited = home_page.go_revoke_deposit_page_if_deposited()
    if deposited is True:
        deposit_record_page.revoke_deposit()

    yield (
        login_page,
        home_page,
        home_bottom_navigator_bar,
        deposit_page,
        deposit_record_page,
        offline_deposit,
        deposit_choose_amount_page,
        deposit_success_page,
        account_page,
        finance_record,
        transaction_detail
    )


    driver.quit()
    log(f'{"*" * 8}Close app{"*" * 8}')
