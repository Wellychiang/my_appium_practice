from common import base
from time import sleep
import allure


class LoginPage(base.Base):
    user = "//*[@resource-id=\"com.stage.mpsy.stg:id/iptEdtAccount\"]"
    pwd = "//*[@resource-id=\"com.stage.mpsy.stg:id/iptEdtPassword\"]"
    login_button = "//*[@resource-id=\"com.stage.mpsy.stg:id/btnLogin\"]"
    go_login_page_button = "//*[@resource-id='com.stage.mpsy.stg:id/txtExperienceNow']"

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

    @allure.step('點擊登入')
    def click_login_button(self):
        self.find_element(self.login_button).click()

    @allure.step('跳過廣告進入登入頁面')
    def skip_ad_page(self):
        sleep(5)
        [self.slide(direction='swipe left') for i in range(4)]
        self.find_element(self.go_login_page_button).click()

