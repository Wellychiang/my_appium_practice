from common import base

import pytest
import allure


class BankcardManagePage(base.Base):

    bankcard_manage =   '//*[contains(@text, "添加银行卡")]'

    bankcard_account =  '//*[@resource-id="com.stage.mpsy.stg:id/txtBankAccount"]'
    bank_name =         '//*[@resource-id="com.stage.mpsy.stg:id/txtBankName"]'
    bankcard_status =   '//*[@resource-id="com.stage.mpsy.stg:id/txtTransStatus"]'

    back_btn =          '//*[@resource-id="com.stage.mpsy.stg:id/btnBack"]'

    @allure.step('點擊添加銀行卡')
    def click_add_bankcard(self):
        self.find_element(self.bankcard_manage).click()

    @allure.step('返回目前銀行卡數量')
    def return_how_many_bankcard_now(self):
        # 因為 find_elements 失效, 只好一個個遍歷
        for count in range(1, 11):
            try:
                assert self.find_element(f'({self.bankcard_account})[{count}]') is not None
            except Exception as e:
                bank_count = count - 1
                print(bank_count)
                return bank_count

    @allure.step('檢查銀行卡賬號')
    def check_bankcard_account(self, bank_account, count=1):
        self.assert_(
            'equal',
            self.find_element(f'({self.bankcard_account})[{count}]').text,
            bank_account
        )

    @allure.step('檢查銀行卡銀行')
    def check_bankcard_bank(self, bank_name, count=1):
        self.assert_(
            'equal',
            self.find_element(f'({self.bank_name})[{count}]').text,
            bank_name
        )

    @allure.step('檢查銀行卡狀態')
    def check_bankcard_status(self, status, count=1):
        self.assert_(
            'in',
            status,
            self.find_element(f'({self.bankcard_status})[{count}]').text
        )

    @allure.step('點擊銀行卡, 進入我的銀行信息頁面')
    def click_bankcard_to_my_bankcard_page(self, bank_account):
        self.find_element(f'//*[contains(@text, "{bank_account}")]').click()

    @allure.step('點擊返回鍵')
    def click_back_btn(self):
        self.find_element(self.back_btn).click()

