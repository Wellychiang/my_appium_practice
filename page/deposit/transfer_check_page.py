from common import base

import allure
import pytest
import time


class TransferCheckPage(base.Base):
    title =                 '//*[@resource-id="com.stage.mpsy.stg:id/topTitle"]'
    name =                  '//*[@resource-id="com.stage.mpsy.stg:id/txtAccount"]'
    amount =                '//*[@resource-id="com.stage.mpsy.stg:id/txtAmount"]'
    post_script =           '//*[@resource-id="com.stage.mpsy.stg:id/txtPostscript"]'

    copy_amount =           '//*[@resource-id="com.stage.mpsy.stg:id/amountCopyImg"]'
    copy_card_num =         '//*[@resource-id="com.stage.mpsy.stg:id/imgBankAccount"]'
    copy_account_name =     '//*[@resource-id="com.stage.mpsy.stg:id/imgBankAccountName"]'
    copy_post_script =      '//*[@resource-id="com.stage.mpsy.stg:id/postscriptCopyImg"]'
    copy_success =          '//*[contains(@text, "复制完成")]'

    img_upload =            '//*[@resource-id="com.stage.mpsy.stg:id/imgUpload"]'
    from_picture_lib =      '(//*[@class="android.widget.LinearLayout"])[2]'
    allowed =               '(//*[contains(@text, "允許")])[2]'
    my_picture =            '//*[@resource-id="com.google.android.documentsui:id/icon_thumb"]'
    confirm_picture =       '//*[@resource-id="com.stage.mpsy.stg:id/menu_crop"]'

    deposit_confirm =       '//*[contains(@text, "我已成功转账")]'


    @allure.step('轉帳之前檢查填入資訊')
    def check_input_info_before_transfer(
            self,
            transfer_method,
            deposit_name,
            deposit_amount,
            name
    ):
        # assert f'{transfer_method} 个人号转账' in self.find_element(self.title).text
        assert self.find_element(self.name).text == deposit_name
        assert int(float(self.find_element(self.amount).text)) == deposit_amount
        print(self.find_element(self.post_script).text)
        assert name[:4].upper() in self.find_element(self.post_script).text

    @allure.step('檢查複製文字功能')
    def check_copy_function(self):
        self.find_element(self.copy_amount).click()
        assert self.find_element(self.copy_success) is not False
        self.find_element(self.copy_card_num).click()
        assert self.find_element(self.copy_success) is not False
        self.find_element(self.copy_account_name).click()
        assert self.find_element(self.copy_success) is not False
        self.find_element(self.copy_post_script).click()
        assert self.find_element(self.copy_success) is not False

    @allure.step('點擊圖片, 跳出選擇圖庫或相片')
    def click_image_btn(self):
        self.find_element(self.img_upload).click()

    @allure.step('點擊從圖庫')
    def click_from_picture_lib(self):
        self.find_element(self.from_picture_lib).click()

    @allure.step('允許從 app 讀取圖庫')
    def allowed_app_load_image(self):
        self.find_element(self.allowed).click()

    @allure.step('選擇圖庫裡第一張照片, 進入修改照片')
    def choose_the_first_in_lib(self):
        self.find_element(self.my_picture).click()

    @allure.step('點擊右上角勾勾, 確認上傳修改完圖片')
    def upload_the_chosen_image(self):
        self.find_element(self.confirm_picture).click()

    @allure.step('點擊我已成功轉賬')
    def click_transfer_success(self):
        self.find_element(self.deposit_confirm).click()
