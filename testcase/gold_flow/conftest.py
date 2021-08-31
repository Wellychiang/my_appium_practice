from appium import webdriver
from common.base import log

from page.login_page import LoginPage
from page.home_page import HomePage


from page.deposit_record_page import DepositRecordPage

from testcase import ims

import pytest
import allure


@allure.step('初始化充值頁面, 已充值帳號')
def setup_settings(playerid):
    deposit_methods = ('offline', 'netbank')

    log(f'\n{"-"*8}Setup settings{"-"*8}')

    for deposit_method in deposit_methods:
        ims.set_up_deposit_page_settings(deposit_method=deposit_method)

    deposit_audit_search = ims.deposit_audit_search(playerid=playerid)
    if deposit_audit_search['total'] != 0 and len(deposit_audit_search['data']) != 0:
        deposit_id = deposit_audit_search['data'][0]['depositid']
        unlock_status = ims.deposit_data_lock_or_not(deposit_id=deposit_id, status='unlock')
        approve_status = ims.deposit_data_approve(deposit_id=deposit_id, ec_remarks='setup')
        if str(unlock_status) != '204' or str(approve_status) != '204':
            raise ValueError(f'IMS unlock status: {unlock_status}\tIMS approve status: {approve_status}')

    log(f'\n{"-"*8}Settings done{"-"*8}')


@pytest.fixture()
def driver(request):
    log(f'\n{"-"*8}Start app{"-"*8}')
    param = request.param
    setup_settings(playerid=param['username'])
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

    deposit_record_page =           DepositRecordPage(driver)

    try:
        login_page.login(account=param['username'], pwd=param['pwd'])

        home_page.ignore_gift_if_it_show_up()
        # TODO: 每日簽到的 skip
        home_page.ignore_ads_if_ads_show_up()
        home_page.click_deposit_button()

        yield driver

    except Exception as e:
        raise ValueError(str(e))
    finally:
        driver.quit()
        deposit_audit_search = ims.deposit_audit_search(playerid=param['username'])
        if deposit_audit_search['total'] != 0 and len(deposit_audit_search['data']) != 0:
            deposit_id = deposit_audit_search['data'][0]['depositid']
            unlock_status = ims.deposit_data_lock_or_not(deposit_id=deposit_id, status='unlock')
            approve_status = ims.deposit_data_approve(deposit_id=deposit_id, ec_remarks='setup')
            if str(unlock_status) != '204' or str(approve_status) != '204':
                raise ValueError(f'IMS unlock status: {unlock_status}\tIMS approve status: {approve_status}')
        log(f'{"-"*8}Close app{"-"*8}')


@pytest.fixture()
def driver_with_deposit_revoke_or_audit(request):
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

    deposit_record_page =        DepositRecordPage(driver)

    login_page.login(account=param['username'], pwd=param['pwd'])

    home_page.ignore_gift_if_it_show_up()
    # TODO: 每日簽到的 skip
    home_page.ignore_ads_if_ads_show_up()
    home_page.click_deposit_button()
    deposited = home_page.go_revoke_deposit_page_if_deposited()
    if deposited is True:
        deposit_record_page.revoke_deposit()

    yield driver

    driver.quit()
    log(f'{"*" * 8}Close app{"*" * 8}')
