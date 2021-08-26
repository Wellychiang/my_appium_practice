from common import base

import time
import allure


class HomePage(base.Base):
    # 登入時的禮物, 或是廣告懸浮視窗
    gift =                  '//*[@resource-id="com.stage.mpsy.stg:id/imgSVGA"]'
    gift_confirm =          '//*[contains(@text, "OK")]'
    floating_ads =          '//*[@resource-id="com.stage.mpsy.stg:id/imgFloatingAds"]'
    close_ads =             '//*[@resource-id="com.stage.mpsy.stg:id/imgFloatingAdsClose"]'

    # 充提
    deposit =               '//*[@resource-id="com.stage.mpsy.stg:id/layoutDeposit"]'
    withdraw =              '//*[@resource-id="com.stage.mpsy.stg:id/layoutWithdraw"]'

    # 提示
    deposit_hint =          '//*[contains(@text, "您尚有存款未批准，请等待批准或撤销存款单")]'
    deposit_hint_close =    '//*[contains(@text, "关闭")]'
    check_deposit_record =  '//*[contains(@text, "查看存款纪录")]'

    # bottom_nav_bar
    home_page =             '//*[@content-desc="首页"]'
    discount =              '//*[@content-desc="优惠"]'
    customer_service =      '//*[@content-desc="客服"]'
    about_us =              '//*[@content-desc="关于我们"]'
    account =               '//*[@content-desc="帐户"]'
    account_new_notification = '//*[@content-desc="帐户, New notification"]'

    @allure.step('點擊開啟禮物, 再點OK跳過')
    def ignore_gift_if_it_show_up(self):
        if self.find_element(self.gift):
            self.find_element(self.gift).click()
            time.sleep(3.5)
            self.android_go_back()
        else:
            pass

    @allure.step('廣告出現就跳過')
    def ignore_ads_if_ads_show_up(self):
        if self.find_element(self.floating_ads):
            self.close_floating_ads()
        else:
            pass

    @allure.step('點擊X, 關閉廣告')
    def close_floating_ads(self):
        self.find_element(self.close_ads).click()

    @allure.step('點擊充值, 進入充值頁面')
    def click_deposit_button(self):
        self.find_element(self.deposit).click()

    @allure.step('跳出已有充值提示, 進入查看存款紀錄並撤銷')
    def go_revoke_deposit_page_if_deposited(self):
        if self.find_element(self.deposit_hint):
            self.find_element(self.deposit_hint_close)
            self.find_element(self.deposit_hint).click()
            self.find_element(self.check_deposit_record).click()
            time.sleep(1)
            return True
        else:
            pass

    @allure.step('跳出已有充值提示, 點擊關閉')
    def click_close_if_deposit_hint_displayed(self):
        if self.find_element(self.deposit_hint):
            self.find_element(self.deposit_hint_close).click()

    @allure.step('點擊提款, 進入提款頁面')
    def click_withdraw_button(self):
        self.find_element(self.withdraw).click()

    # bottom_nav_bar
    @allure.step('檢查底部導覽列都存在')
    def check_bottom_navigator_display(self):
        assert self.find_element(self.home_page) is not None
        assert self.find_element(self.discount) is not None
        assert self.find_element(self.customer_service) is not None
        assert self.find_element(self.about_us) is not None
        if self.find_element(self.account_new_notification):
            pass
        else:
            assert self.find_element(self.account) is not None

    @allure.step('進入賬戶')
    def go_to_account(self):
        if self.find_element(self.account_new_notification):
            self.find_element(self.account_new_notification).click()
        else:
            self.find_element(self.account).click()




