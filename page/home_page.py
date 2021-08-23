from common import base

import time
import allure


class HomePage(base.Base):
    gift =                  '//*[@resource-id="com.stage.mpsy.stg:id/imgSVGA"]'
    gift_confirm =          '//*[contains(@text, "OK")]'
    floating_ads =          '//*[@resource-id="com.stage.mpsy.stg:id/imgFloatingAds"]'
    close_ads =             '//*[@resource-id="com.stage.mpsy.stg:id/imgFloatingAdsClose"]'

    deposit =               '//*[@resource-id="com.stage.mpsy.stg:id/layoutDeposit"]'
    deposit_hint =          '//*[contains(@text, "您尚有存款未批准，请等待批准或撤销存款单")]'
    check_deposit_record =  '//*[contains(@text, "查看存款纪录")]'

    withdraw =              '//*[@resource-id="com.stage.mpsy.stg:id/layoutWithdraw"]'

    @allure.step('點擊開啟禮物, 再點OK跳過')
    def ignore_gift_if_it_show_up(self):
        if self.find_element(self.gift):
            self.find_element(self.gift).click()
            self.find_element(self.gift_confirm).click()
        else:
            pass

    @allure.step('廣告出現就跳過')
    def ignore_ads_if_ads_show_up(self):
        if self.find_element(self.floating_ads) is not None:
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
            self.find_element(self.deposit_hint).click()
            self.find_element(self.check_deposit_record).click()
            time.sleep(1)
            return True
        else:
            pass

    @allure.step('點擊提款, 進入提款頁面')
    def click_withdraw_button(self):
        self.find_element(self.withdraw).click()



    class BottomNavigatorBar(base.Base):
        home_page =         '//*[@content-desc="首页"]'
        discount =          '//*[@content-desc="优惠"]'
        customer_service =  '//*[@content-desc="客服"]'
        about_us =          '//*[@content-desc="关于我们"]'
        account =           '//*[@content-desc="帐户"]'

        account_new_notification = '//*[@content-desc="帐户, New notification"]'

        def check_bottom_navigator_display(self):
            assert self.find_element(self.home_page) is not None
            assert self.find_element(self.discount) is not None
            assert self.find_element(self.customer_service) is not None
            assert self.find_element(self.about_us) is not None
            assert self.find_element(self.account) is not None

