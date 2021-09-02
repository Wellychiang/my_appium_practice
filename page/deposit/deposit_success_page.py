from common import base

import allure
import pytest


class DepositSuccessPage(base.Base):
    title =                 '//*[@resource-id="com.stage.mpsy.stg:id/titleSuccess"]'
    amount =                '//*[@resource-id="com.stage.mpsy.stg:id/txtAmount"]'
    deposit_id =            '//*[@resource-id="com.stage.mpsy.stg:id/txtOrder"]'
    time =                  '//*[@resource-id="com.stage.mpsy.stg:id/txtOrderTime"]'
    deposit_name =          '//*[@resource-id="com.stage.mpsy.stg:id/txtAccount"]'
    method =                '//*[@resource-id="com.stage.mpsy.stg:id/txtBankOut"]'
    receive_payment_bank =  '//*[@resource-id="com.stage.mpsy.stg:id/txtReceiveAccount"]'
    deposit_bank =          '//*[@resource-id="com.stage.mpsy.stg:id/txtOption1"]'

    close =                 '//*[@resource-id="com.stage.mpsy.stg:id/btnCancel"]'
    go_deposit_record =     '//*[@resource-id="com.stage.mpsy.stg:id/btnRecord"]'

    @allure.step('點擊關閉後, 返回首頁')
    def click_close_and_go_back_to_home_page(self):
        self.find_element(self.close).click()

    @allure.step('檢查成功申請的存款項目, return 訂單號(deposit_id)')
    def check_all_info_with_success_deposited(
            self,
            amount,
            deposit_name,
            receive_payment_bank,
            # transfer_out_bank
    ):
        """
        參數由使用這個方法的一方提供
        """

        self.assert_('equal', int(float(self.find_element(self.amount).text)), int(amount))
        self.assert_('equal', self.find_element(self.deposit_name).text, deposit_name)
        self.assert_('in', receive_payment_bank, self.find_element(self.receive_payment_bank).text)
        # assert self.find_element(self.deposit_bank).text == transfer_out_bank

        return self.find_element(self.deposit_id).text

