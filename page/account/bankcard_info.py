from common import base

import pytest
import allure


class BankcardInfo(base.Base):
    card_name = '//*[@resource-id="com.stage.mpsy.stg:id/edtAccountName"]'
    bank_name = '//*[@resource-id="com.stage.mpsy.stg:id/spSelectBank"]'
    subbank_name = '//*[@resource-id="com.stage.mpsy.stg:id/edtBranch"]'
    bank_account = '//*[@resource-id="com.stage.mpsy.stg:id/edtBankAccount"]'
    IFSC = '//*[@resource-id="com.stage.mpsy.stg:id/edtProvince"]'

    login_pwd = '//*[@resource-id="com.stage.mpsy.stg:id/edtLoginPassword"]'
    confirm_update = '//*[@resource-id="com.stage.mpsy.stg:id/btnConfirm"]'

    success_info = '//*[contains(@text, "编辑银行卡成功")]'

    @allure.step('輸入登入密碼')
    def input_pwd(self, pwd):
        self.find_element(self.login_pwd).send_keys(pwd)

    @allure.step('點擊確認, 修改我的銀行信息')
    def click_confirm_to_update_my_bankcard_info(self):
        self.find_element(self.confirm_update).click()

    @allure.step('檢查 "编辑银行卡成功" 信息')
    def check_edit_bankcard_success_hint(self):
        assert self.find_element(self.success_info) is not False

