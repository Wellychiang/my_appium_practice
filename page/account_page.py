from common import base

import allure
import pytest


class AccountPage(base.Base):
    finance_record = '//*[contains(@text, "财务纪录")]'

    @allure.step('進入財務紀錄')
    def go_to_finance_record(self):
        self.find_element(self.finance_record).click()

    class FinanceRecord(base.Base):
        top_layout =    {
            'title':    '//*[contains(@text, "财务纪录")]',
            'back_key': '//*[@resource-id="com.stage.mpsy.stg:id/btnBack"]'
        }
        condition_layout = {
            'filter': {
                'btn': '//*[@resource-id="com.stage.mpsy.stg:id/selectType"]',
                'type': {
                    'deposit':      '//*[contains(@text, "充值")]',
                    'withdraw':     '//*[contains(@text, "提现")]',
                    'promotion':    '//*[contains(@text, "优惠")]'
                },
            },
            'select_day_btn': '//*[@resource-id="com.stage.mpsy.stg:id/selectDate"]',
            'select_day':    ''
        }
        # content layout
        trans_title = '//*[@resource-id="com.stage.mpsy.stg:id/txtTransTitle"]'
        trans_status = '//*[@resource-id="com.stage.mpsy.stg:id/txtTransStatus"]'
        trans_amount = '//*[@resource-id="com.stage.mpsy.stg:id/txtTransAmount"]'


        @allure.step('打開搜尋條件類型清單')
        def click_to_show_up_condition_type_list(self):
            # 因 select_condition_type() 抓不到, 所以這個先用不到
            self.find_element(self.condition_layout['filter']['btn']).click()

        @allure.step('選擇搜尋條件類型')
        def select_condition_type(self, type_):
            # TODO: Appium, uiautomator viewer抓不到, weditor 抓的到但跑起來的時候 appium 似乎因為本身不支援所以還是抓不到
            # 所以先不用這個
            print(self.condition_layout['filter']['type'][type_])
            self.find_element(self.condition_layout['filter']['type'][type_]).click()

        @allure.step('檢查充值單據第幾筆的狀態, 錢')
        def check_deposit_info(self, count, title, status, amount):
            assert self.find_element(f"({self.trans_title})[{count}]").text == title
            assert self.find_element(f"({self.trans_status})[{count}]").text == status
            assert self.find_element(f"({self.trans_amount})[{count}]").text == str(amount) + '.00'

        @allure.step('點擊第幾筆選擇的單據, 進入交易詳情')
        def enter_to_deposit_detail(self, count):
            self.find_element(f"({self.trans_amount})[{count}]").click()


        class TransactionDetail(base.Base):
            @allure.step('檢查金額')
            def check_amount(self, amount):
                assert self.find_element(f'//*[contains(@text, "{amount}.00"]') is not None

            @allure.step('檢查狀態')
            def check_status(self, status):
                assert self.find_element(f'//*[contains(@text, "{status}"]') is not None

            @allure.step('檢查備註')
            def check_remark(self, remark):
                assert self.find_element(f'//*[contains(@text, "{remark}"]') is not None

