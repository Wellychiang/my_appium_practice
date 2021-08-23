from common import base

import allure


class DepositPage(base.Base):

    class MethodChoose(base.Base):
        offline =   '//*[contains(@text,"线下入款")]'
        netbank =   '//*[contains(@text,"网银转账")]'
        borrow =    '//*[contains(@text,"借记卡")]'
        momo =      '//*[contains(@text,"Momo Pay")]'
        Zalo =      '//*[contains(@text,"Zalo Pay")]'
        viettel =   '//*[contains(@text,"Viettel Pay")]'
        upi =       '//*[contains(@text,"UPI")]'
        paytm =     '//*[contains(@text,"Paytm")]'
        bhim =      '//*[contains(@text,"BHIM")]'
        wechat =    '//*[contains(@text,"微信支付")]'
        neteller =  '//*[contains(@text,"Neteller")]'
        skrill =    '//*[contains(@text,"Skrill")]'
        alipay =    '//*[contains(@text,"支付宝")]'
        qq =        '//*[contains(@text,"QQ钱包")]'
        quick =     '//*[contains(@text,"快捷支付")]'
        qrcode =    '//*[contains(@text,"扫码/H5支付")]'

        @allure.step('點擊使用付款方式')
        def choose_pay_method(self, method):
            self.find_element(f'//*[contains(@text,"{method}")]').click()


    class ReceivePaymentBank(base.Base):
        bank_choose =   '//*[@resource-id="com.stage.mpsy.stg:id/transInBankTitleName"]'
        buttom_sheet =  '//*[@resource-id="com.stage.mpsy.stg:id/design_bottom_sheet"]'

        @allure.step('點擊收款銀行, 從底部彈出銀行清單')
        def click_to_show_up_bank_list(self):
            self.find_element(self.bank_choose).click()
            self.display_bank_list_or_not(display=True)

        @allure.step('選擇充值銀行')
        def click_to_choose_bank(self, bank_name='成都银行'):
            self.find_element(f'//*[contains(@text, "{bank_name}")]').click()

        @allure.step('檢查銀行清單是否彈出')
        def display_bank_list_or_not(self, display):
            if display is False:
                assert self.find_element(self.buttom_sheet) is None
            elif display is True:
                assert self.find_element(self.buttom_sheet) is not None

    class BankDetail(base.Base):
        post_script = '//*[@resource-id="com.stage.mpsy.stg:id/txtPostscript"]'
        next_step =   '//*[@text="下一步"]'

        @allure.step('顯示已選的銀行')
        def check_bank_name_when_its_chosen(self, bank_name='成都银行'):
            assert self.find_element(f'//*[contains(@text, "{bank_name}")]') is not None

        @allure.step('顯示已選銀行的分行')
        def check_subbank_name_when_its_chosen(self, subbank_name='上海分行'):
            assert self.find_element(f'//*[contains(@text, "{subbank_name}")]') is not None

        @allure.step('顯示附言為使用者名稱')
        def check_post_script(self, username: str):
            assert self.find_element(self.post_script).text == str(username).upper()

        @allure.step('點擊下一步, 進入選擇金額頁面')
        def click_next_step(self):
            self.find_element(self.next_step).click()


    class ChooseAmountPage(base.Base):
        popup_hint_title =      '//*[@resource-id="com.stage.mpsy.stg:id/txtTitle"]'
        popup_hint_message =    '//*[@resource-id="com.stage.mpsy.stg:id/txtMessage"]'
        popup_hint_confirm =    '//*[@resource-id="com.stage.mpsy.stg:id/txtConfirm"]'

        name =                  '//*[@resource-id="com.stage.mpsy.stg:id/edtName"]'
        remark =                '//*[@resource-id="com.stage.mpsy.stg:id/edtRemark"]'
        immediately_deposit =   '//*[contains(@text, "立即存款")]'

        # 以下為一組(點擊後有展開後續動作)
        deposit_method =        '//*[@resource-id="com.stage.mpsy.stg:id/depositMethodArrow"]'
        ATM_transger =          '//*[contains(@text, "ATM 转帐")]'
        ATM_cash =              '//*[contains(@text, "ATM 现金存入")]'
        bank_counter =          '//*[contains(@text, "银行柜檯")]'
        another =               '//*[contains(@text, "其他")]'

        transfer_out_bank =     '//*[@resource-id="com.stage.mpsy.stg:id/transBankArrow"]'

        img =                   '//*[@resource-id="com.stage.mpsy.stg:id/imgUploadOffline"]'
        from_picture_lib =      '(//*[@class="android.widget.LinearLayout"])[2]'
        allowed =               '(//*[contains(@text, "允許")])[2]'
        my_picture =            '//*[@resource-id="com.google.android.documentsui:id/icon_thumb"]'
        confirm_picture =       '//*[@resource-id="com.stage.mpsy.stg:id/menu_crop"]'

        other_amount =          '//*[contains(@text, "其它金额")]'
        amount_placeholder =    '//*[@resource-id="com.stage.mpsy.stg:id/edtCustomAmount"]'


        @allure.step('檢查溫馨提示訊息並點擊確定, 關閉提示視窗')
        def check_popup_warm_hint_and_click_confirm(self):
            assert self.find_element(self.popup_hint_title).text == '温馨提示'
            assert '公司账号随时更换! 请每次存款都至入款画面进行操作' in self.find_element(self.popup_hint_message).text
            self.find_element(self.popup_hint_confirm).click()

        @allure.step('輸入存款人姓名')
        def input_name(self, name):
            self.find_element(self.name).clear()
            self.find_element(self.name).send_keys(name)

        @allure.step('點開轉出銀行的銀行選單')
        def click_to_show_up_transfer_out_bank_list(self):
            self.find_element(self.transfer_out_bank).click()

        @allure.step('選擇轉出銀行')
        def choose_transfer_out_bank(self, bank_name='平安银行'):
            self.find_element(f'//*[@text="{bank_name}"]').click()

        @allure.step('輸入存款備註')
        def input_remark(self, remark):
            self.find_element(self.remark).send_keys(remark)

        @allure.step('上傳圖片')
        def upload_img(self):
            self.find_element(self.img).click()
            self.find_element(self.from_picture_lib).click()
            self.find_element(self.allowed).click()

            self.find_element(self.img).click()
            self.find_element(self.from_picture_lib).click()
            self.find_element(self.my_picture).click()
            self.find_element(self.confirm_picture).click()

        @allure.step('選擇其他金額後(立即存款變成無法點擊), 並輸入想要的金額(輸入後立即存款可以點擊)')
        def choose_other_amount_button_then_input_amount(self, amount):
            self.find_element(self.other_amount).click()
            self.check_immediately_deposit_is_enabled_or_not(bool_=False)

            self.find_element(self.amount_placeholder).send_keys(amount)
            self.check_immediately_deposit_is_enabled_or_not(bool_=True)

        @allure.step('確定立即存款按鈕可否點擊')
        def check_immediately_deposit_is_enabled_or_not(self, bool_):
            assert self.find_element(self.immediately_deposit).is_enabled() is bool_

        @allure.step('點擊立即存款')
        def click_immediately_deposit(self,):
            self.find_element(self.immediately_deposit).click()


    class DepositSuccessPage(base.Base):
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
                transfer_out_bank
        ):
            """
            參數由使用這個方法的一方提供
            """
            assert int(float(self.find_element(self.amount).text)) == int(amount)
            assert self.find_element(self.deposit_name).text == deposit_name
            assert receive_payment_bank in self.find_element(self.receive_payment_bank).text
            assert self.find_element(self.deposit_bank).text == transfer_out_bank

            return self.find_element(self.deposit_id).text


