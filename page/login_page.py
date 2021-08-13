from common import base
from time import sleep
import allure


class LoginPage(base.Base):
    AE_logo =               '//*[@resource-id="com.stage.mpsy.stg:id/imgLogo"]'

    login_form =            '//*[@content-desc="登录"]'
    register_form =         '//*[@content-desc="注册"]'

    user =                  '//*[@resource-id="com.stage.mpsy.stg:id/iptEdtAccount"]'
    pwd =                   '//*[@resource-id="com.stage.mpsy.stg:id/iptEdtPassword"]'
    remember_me =           '//*[@resource-id="com.stage.mpsy.stg:id/chkSaveAccount"]'
    forgot_pwd =            '//*[@resource-id="com.stage.mpsy.stg:id/txtForgotPassword"]'
    login_button =          '//*[@resource-id="com.stage.mpsy.stg:id/btnLogin"]'
    go_login_page_button =  "//*[@resource-id='com.stage.mpsy.stg:id/txtExperienceNow']"
    go_browse =             '//*[@resource-id="com.stage.mpsy.stg:id/txtGoBrowse"]'

    def login(self, account, pwd):
        self.skip_ad_page()
        self.input_username(account)
        self.input_pwd(pwd)
        self.click_login_button()

    @allure.step('輸入帳號')
    def input_username(self, account):
        self.find_element(self.user).send_keys(account)

    @allure.step('輸入密碼')
    def input_pwd(self, pwd):
        self.find_element(self.pwd).send_keys(pwd)

    @allure.step('點擊記住我')
    def click_remember_me(self):
        self.find_element(self.remeber_me).click()

    @allure.step('點擊忘記密碼')
    def click_forgot_pwd(self):
        self.find_element(self.forgot_pwd).click()

    @allure.step('點擊登入, 進入首頁')
    def click_login_button(self):
        self.find_element(self.login_button).click()

    @allure.step('跳過廣告進入登入頁面')
    def skip_ad_page(self):
        sleep(5)
        [self.slide(direction='swipe left') for i in range(4)]
        self.find_element(self.go_login_page_button).click()

    @allure.step('點擊註冊表單')
    def click_register_form(self):
        self.find_element(self.register_form).click()

    @allure.step('點擊登入表單')
    def click_login_form(self):
        self.find_element(self.login_form).click()

    @allure.step('點擊先去逛逛, 進入首頁')
    def click_go_browse(self):
        self.find_element(self.go_browse).click()
