from common import base

import allure
import pytest


class AccountPage(base.Base):
    finance_record = '//*[contains(@text, "财务纪录")]'
    bankcard_manage = '//*[contains(@text, "银行卡管理")]'

    @allure.step('進入財務紀錄')
    def go_to_finance_record(self):
        self.find_element(self.finance_record).click()

    @allure.step('進入銀行卡管理')
    def go_to_bankcard_manage(self):
        self.find_element(self.bankcard_manage).click()

