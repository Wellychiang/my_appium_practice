from common import base

import allure


class DepositRecordPage(base.Base):
    revoke =            '//*[contains(@text, "撤销")]'
    revoke_confirm =    '//*[@resource-id="com.stage.mpsy.stg:id/txtConfirm"]'

    revoke_success =    'xx'
    success_confirm =   '//*[contains(@text, "确定")]'

    @allure.step('點擊撤銷之後點擊確定')
    def revoke_deposit(self):
        self.find_element(self.revoke).click()
        self.find_element(self.revoke_confirm).click()

        # TODO: 補上 revoke_success xpath 用來檢查
        self.find_element(self.success_confirm).click()
