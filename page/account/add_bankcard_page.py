from common import base

import allure
import pytest


class AddBankcardPage(base.Base):

    bank_choose =       '//*[@resource-id="com.stage.mpsy.stg:id/textItem"]'
    bank_account =      '//*[@resource-id="com.stage.mpsy.stg:id/edtBankAccount"]'

    img_upload =        '//*[@resource-id="com.stage.mpsy.stg:id/imgPic3"]'
    from_picture_lib =  '(//*[@class="android.widget.LinearLayout"])[2]'
    allowed =           '(//*[contains(@text, "允許")])[2]'
    my_picture =        '//*[@resource-id="com.google.android.documentsui:id/icon_thumb"]'
    confirm_picture =   '//*[@resource-id="com.stage.mpsy.stg:id/menu_crop"]'

    confirm_btn =       '//*[@resource-id="com.stage.mpsy.stg:id/btnConfirm"]'

    @allure.step('點擊請選擇, 彈出銀行清單')
    def click_to_show_up_bank_list(self):
        self.find_element(self.bank_choose).click()

    @allure.step('從銀行清單中選擇銀行')
    def choose_bank(self, bank_name='平安银行'):
        self.find_element(f'//*[contains(@text, "{bank_name}")]').click()

    @allure.step('輸入銀行賬號')
    def input_bank_account(self, bank_account):  # 6 ~ 22 int
        self.find_element(self.bank_account).send_keys(bank_account)

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

    @allure.step('點擊確定')
    def click_confirm_btn(self):
        self.find_element(self.confirm_btn).click()

    @allure.step('檢查完成新增賬號訊息')
    def check_add_bankcard_success_msg(self):
        assert self.find_element('//*[contains(@text, "完成新增银行账号")]') is not False

