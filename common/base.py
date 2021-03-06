from selenium.webdriver.support.ui import WebDriverWait
from allure_commons.types import AttachmentType

import allure
import time
import logging

log_path = 'log/log.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')

console_log = logging.StreamHandler()  # sys.stdout
logger.addHandler(console_log)

file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

log = lambda x: logger.info(str(x).encode('utf-8', 'replace').decode('cp950', 'ignore'))


class Base:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, args):
        try:
            WebDriverWait(self.driver, 13).until(lambda driver: driver.find_element_by_xpath(args)).is_displayed()
            return self.driver.find_element_by_xpath(args)
        except:
            self.get_screen_shot()
            log(f'Can not find {args} element')

    def find_elements(self, args):
        try:
            WebDriverWait(self.driver, 13).until(lambda driver: driver.find_elements_by_xpath(args)).is_displayed()
            return self.driver.find_elements_by_xpath(args)
        except:
            self.get_screen_shot()
            log(f'Can not find {args} element')

    def find_id(self, args):
        try:
            WebDriverWait(self.driver, 13).until(lambda driver: driver.find_element_by_id(args)).is_displayed()
            return self.driver.find_element_by_id(args)
        except:
            self.get_screen_shot()
            raise ValueError(f'Can not find {args} element')

    def slide(self, direction, time=200):
        screen_size = self.driver.get_window_size(self)

        if direction == 'swipe left':
            x1 = screen_size['width'] * 0.75
            y1 = screen_size['height'] * 0.5
            x2 = screen_size['width'] * 0.25
            self.driver.swipe(x1, y1, x2, y1, time)
        elif direction == 'swipe up':
            x1 = screen_size['width'] * 0.5
            y1 = screen_size['height'] * 0.75
            y2 = screen_size['height'] * 0.25
            self.driver.swipe(x1, y1, x1, y2, time)
            print('sliddddd')

    def get_screen_shot(self):
        time_ = time.strftime('%Y-%m-%d %H:%M:%S')
        time_string = ''
        for str_ in time_:
            if str_ in (' ', '-', ':'):
                continue
            else:
                time_string += str_

        file_name = f'screenshot/{time_string}.png'
        self.driver.get_screenshot_as_file(filename=file_name)

        allure.attach.file(
            source=f'screenshot/{time_string}.png',
            name=time_string,
            attachment_type=AttachmentType.PNG
        )

    def assert_(self, method='equal', item='item', target='target', ):
        if method == 'equal':
            if item != target:
                self.get_screen_shot()
                raise AssertionError(f'{item} != {target}')
        elif method == 'not equal':
            if item == target:
                self.get_screen_shot()
                raise AssertionError(f'{item} != {target}')
        elif method == 'in':
            if item not in target:
                self.get_screen_shot()
                raise AssertionError(f'{item} not in {target}')
        elif method == 'is not None':
            if item is None:
                self.get_screen_shot()
                raise AssertionError(f'Element: {item}')

    @allure.step('?????? android ?????????')
    def android_go_back(self):
        self.driver.back()


class Ims:
    import requests

    s = requests.session()

    def __init__(self, env='stg'):
        self.base = f'https://ae-boapi.{env}devops.site/ae-ims/api/v1/'

        self.login =            self.base + 'login'
        self.paymentInfo =      self.base + 'deposits/setting/paymentInfoTemplate'
        self.deposit_audit =    self.base + 'deposits/search'
        self.player_payments =  self.base + 'playerpayments'
        self.withdraw_audit =   self.base + 'withdrawals/search'

    @allure.step('IMS ??????')
    def ims_login(self):
        url = self.login

        username = 'wellytest'
        pwd = 'dc18f76e9b59a3f84eb453cba8c2749d3e6b1eeb'
        # username = 'wellyadmin'
        # pwd = '53aaee23e7afbe47aaf922096a8aca7f886356c5'

        headers = {
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
        }

        data = {"userid": username, "password": pwd}

        r = self.s.post(url, headers=headers, json=data, verify=False)
        log(f'\nStatus: {r.status_code}, Admin: {username}\nIms login: {r.json()}')
        return r.status_code, r.json()

    def get_payment_info(self, token):
        url = self.paymentInfo
        headers = {
            'accept-encoding': 'accept-encoding: gzip, deflate, br',
            'authorization': token
        }

        r = self.s.get(url, headers=headers)

    @allure.step('IMS ????????????????????????')
    def set_up_deposit_page_settings(self, deposit_method='offline'):
        """
        payload ?????? templates ????????????????????? ????????????, ???????????????"???????????????"???"????????????",
        ???????????????????????????????????????????????? api
        method_id:
            -offline: 21906902-493c-4ff6-a6dd-f8430028f5e7
            -Neteller: 7cc19253-4746-47a0-8d89-80e6da5a8e36
        """
        method_id = ''
        payload = ''
        if deposit_method == 'offline':
            method_id = '21906902-493c-4ff6-a6dd-f8430028f5e7'
            payload = {
                "templates": [
                    {
                        "parameterId": "65206de3-8aaf-469f-9750-fce6bc3df8a3",
                        "parameterName": {
                            "en-US": "Beneficiary Name",
                            "hi-IN": "QA-???????????????????????? ?????? ?????????",
                            "id-ID": "QA-Nama Penerima",
                            "ja-JP": "QA-????????????",
                            "ms-MY": "QA-Beneficiary Name",
                            "pt-BR": "QA-Nome do beneficiado",
                            "th-TH": "QA-???????????????????????????????????????",
                            "vi-VN": "QA-Ch??? t??i kho???n",
                            "zh-CN": "????????????",
                            "zh-TW": "????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "d8397e6b-f1dd-4383-8dd2-c0f855051042",
                        "parameterName": {
                            "en-US": "Bank Account",
                            "hi-IN": "QA-???????????? ????????????",
                            "id-ID": "QA-Akun bank",
                            "ja-JP": "QA-????????????",
                            "ms-MY": "QA-Bank Account",
                            "pt-BR": "QA-N??mero do cart??o banc??rio",
                            "th-TH": "QA-??????????????????????????????????????????",
                            "vi-VN": "QA-S??? t??i kho???n",
                            "zh-CN": "????????????",
                            "zh-TW": "????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "63075d89-4284-44e8-937b-ddff782a276a",
                        "parameterName": {
                            "en-US": "Branch",
                            "hi-IN": "QA-??????????????????",
                            "id-ID": "QA-Cabang",
                            "ja-JP": "QA-??????",
                            "ms-MY": "QA-Branch",
                            "pt-BR": "QA-Nome da agencia",
                            "th-TH": "QA-????????????????????????",
                            "vi-VN": "QA-Chi nh??nh",
                            "zh-CN": "??????",
                            "zh-TW": "??????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "4d139ea8-d593-4ec5-b8b9-6cf1e815f8ab",
                        "parameterName": {
                            "en-US": "IFSC Code",
                            "hi-IN": "QA-IFSC Code",
                            "id-ID": "QA-IFSC Code",
                            "ja-JP": "QA-IFSC Code",
                            "ms-MY": "QA-IFSC Code",
                            "pt-BR": "QA-IFSC Code",
                            "th-TH": "QA-IFSC Code",
                            "vi-VN": "QA-IFSC Code",
                            "zh-CN": "IFSC Code",
                            "zh-TW": "IFSC Code"
                        },
                        "ecEnable": True,
                        "parameterRequired": False,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "3b6c24a0-f4c5-42d8-9a82-5ff5a851f31c",
                        "parameterName": {
                            "en-US": "Postscript",
                            "hi-IN": "QA-???????????????????????? ?????????",
                            "id-ID": "QA-Postscript",
                            "ja-JP": "QA-??????",
                            "ms-MY": "QA-Postscript",
                            "pt-BR": "QA-observa????o",
                            "th-TH": "QA-????????????????????????",
                            "vi-VN": "QA-N???i Dung Chuy???n ti???n",
                            "zh-CN": "??????",
                            "zh-TW": "??????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "Please enter the postscript in the bank transfer remark field",
                            "hi-IN": "QA-??????????????? ???????????????????????? ????????????????????? ??????????????????????????? ??????????????? ??????????????? ??????????????????????????????",
                            "id-ID": "QA-Silahkan masukkan postscript di kolom komentar transfer bank",
                            "ja-JP": "QA-???????????????????????????????????????????????????????????????",
                            "ms-MY": "QA-Sila masukkan nota-nota dalam bidang pernyataan pemindahan bank",
                            "pt-BR": "QA-Certifique-se de colar a anota????o acima no campo de coment??rios / observa????o",
                            "th-TH": "QA-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????",
                            "vi-VN": "QA-Y??u C???u Nh???p ????ng Ghi Ch?? N??y Trong N???i Dung Chuy???n Kho???n Ng??n H??ng",
                            "zh-CN": "??????????????????/??????????????????????????????",
                            "zh-TW": "QA-??????????????????/??????????????????????????????"
                        },
                        "otherSetting": {
                            "postscriptRule": "PLAYER_ID_ORIGINAL"
                        }
                    },
                    {
                        "parameterId": "23095923-c372-4732-9128-d037d32bbf49",
                        "parameterName": {
                            "en-US": "Deposit Method",
                            "hi-IN": "QA-????????? ??????????????????",
                            "id-ID": "QA-Tipe Deposit",
                            "ja-JP": "QA-???????????????",
                            "ms-MY": "QA-Deposit Method",
                            "pt-BR": "QA-forma de dep??sito",
                            "th-TH": "QA-??????????????????????????????????????????",
                            "vi-VN": "QA-Ph????ng th???c n???p",
                            "zh-CN": "????????????",
                            "zh-TW": "????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "0b524f22-02ce-4e7d-abea-ebb2dbb9b3ee",
                        "parameterName": {
                            "en-US": "Amount",
                            "hi-IN": "QA-Amount",
                            "id-ID": "QA-Jumlah",
                            "ja-JP": "QA-???",
                            "ms-MY": "QA-Amount",
                            "pt-BR": "QA-Valor do dep??sito",
                            "th-TH": "QA-?????????????????????????????????????????????",
                            "vi-VN": "QA-Nh???p s??? ti???n",
                            "zh-CN": "????????????",
                            "zh-TW": "????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "d9507b7f-9463-41fb-9d3a-5e1e4a006cd1",
                        "parameterName": {
                            "en-US": "Deposit Time",
                            "hi-IN": "QA-????????? ?????????",
                            "id-ID": "QA-Waktu Deposit",
                            "ja-JP": "QA-????????????",
                            "ms-MY": "QA-Deposit Time",
                            "pt-BR": "QA-Hor??rio do dep??sito",
                            "th-TH": "QA-?????????????????????????????????",
                            "vi-VN": "QA-Th???i gian g???i",
                            "zh-CN": "????????????",
                            "zh-TW": "????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "07643418-c1eb-442a-b852-0f088f46015b",
                        "parameterName": {
                            "en-US": "Depositor Name",
                            "hi-IN": "QA-???????????????????????? ?????? ?????????",
                            "id-ID": "QA-Nama Deposit",
                            "ja-JP": "QA-????????????",
                            "ms-MY": "QA-Depositor Name",
                            "pt-BR": "QA-Nome do depositante",
                            "th-TH": "QA-???????????????????????????????????????????????????",
                            "vi-VN": "QA-H??? t??n ng?????i g???i",
                            "zh-CN": "???????????????",
                            "zh-TW": "???????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "",
                            "hi-IN": "",
                            "id-ID": "",
                            "ja-JP": "",
                            "ms-MY": "",
                            "pt-BR": "",
                            "th-TH": "",
                            "vi-VN": "Ti???ng Vi???t Ti???ng Vi???t",
                            "zh-CN": "QA-depositName????????????",
                            "zh-TW": ""
                        },
                        "otherSetting": None
                    },
                    {
                        "parameterId": "a1c8b3ae-789b-4883-a0d8-e1722bdc843b",
                        "parameterName": {
                            "en-US": "Transfer from",
                            "hi-IN": "QA-Transfer from",
                            "id-ID": "QA-Transfer Dari",
                            "ja-JP": "QA-?????????",
                            "ms-MY": "QA-Transfer from",
                            "pt-BR": "QA-banco de origem",
                            "th-TH": "QA-????????????????????????????????????",
                            "vi-VN": "QA-Ng??n h??ng chuy???n",
                            "zh-CN": "????????????",
                            "zh-TW": "????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "Please select",
                            "hi-IN": "QA-??????????????? ??????????????????",
                            "id-ID": "QA-Silahkan pilih",
                            "ja-JP": "QA-????????????????????????",
                            "ms-MY": "QA-Sila pilih",
                            "pt-BR": "QA-favor selecione",
                            "th-TH": "QA-???????????????????????????",
                            "vi-VN": "QA-Ch???n ng??n h??ng",
                            "zh-CN": "?????????",
                            "zh-TW": "QA-?????????"
                        },
                        "otherSetting": None
                    },
                    {
                        "parameterId": "9d39ad85-628f-49f4-aa3e-74d401771bef",
                        "parameterName": {
                            "en-US": "Remarks",
                            "hi-IN": "QA-Remarks",
                            "id-ID": "QA-Remarks",
                            "ja-JP": "QA-Remarks",
                            "ms-MY": "QA-Remarks",
                            "pt-BR": "QA-Remarks",
                            "th-TH": "QA-???????????????????????????",
                            "vi-VN": "QA-Nh???n x??t",
                            "zh-CN": "????????????",
                            "zh-TW": "????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": False,
                        "parameterTips": {
                            "en-US": "",
                            "hi-IN": "",
                            "id-ID": "",
                            "ja-JP": "",
                            "ms-MY": "",
                            "pt-BR": "",
                            "th-TH": "",
                            "vi-VN": "",
                            "zh-CN": "QA-remarks????????????",
                            "zh-TW": ""
                        },
                        "otherSetting": None
                    },
                    {
                        "parameterId": "9cae777a-ad76-4fe0-8b79-6ba3a4633350",
                        "parameterName": {
                            "en-US": "Upload Deposit Proof",
                            "hi-IN": "QA-?????????????????? ??????????????? ????????????",
                            "id-ID": "QA-Unduh Struk Pembayaran",
                            "ja-JP": "QA-??????????????????",
                            "ms-MY": "QA-Upload Deposit Proof",
                            "pt-BR": "QA-Carregar captura de tela",
                            "th-TH": "QA-???????????????????????????????????????????????????",
                            "vi-VN": "QA-T???i h??a ????n",
                            "zh-CN": "????????????",
                            "zh-TW": "????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": False,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "bfdb27e8-8e44-4220-86af-fa6147872d2c",
                        "parameterName": {
                            "en-US": "Reminder",
                            "hi-IN": "Reminder",
                            "id-ID": "Reminder",
                            "ja-JP": "Reminder",
                            "ms-MY": "Reminder",
                            "pt-BR": "Reminder",
                            "th-TH": "?????????????????????????????????",
                            "vi-VN": "L??u ??",
                            "zh-CN": "????????????",
                            "zh-TW": "bankId"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "Please enter your name correctly",
                            "hi-IN": "",
                            "id-ID": "",
                            "ja-JP": "",
                            "ms-MY": "",
                            "pt-BR": "",
                            "th-TH": "",
                            "vi-VN": "",
                            "zh-CN": "??????????????????????????????????????????????????????",
                            "zh-TW": ""
                        },
                        "otherSetting": None
                    }
                ]
            }
        elif deposit_method == 'Neteller':
            method_id = '7cc19253-4746-47a0-8d89-80e6da5a8e36'
            payload = {
                "templates": [
                    {
                        "parameterId": "16cb6bee-b586-4b66-988a-33338dbca6eb",
                        "parameterName": {
                            "en-US": "QA-Account Name",
                            "hi-IN": "QA-???????????? ?????????",
                            "id-ID": "QA-Akun",
                            "ja-JP": "QA-???????????????",
                            "ms-MY": "QA-Nama akaun",
                            "pt-BR": "QA-Nome da conta",
                            "th-TH": "QA-???????????????",
                            "vi-VN": "QA-T??n ng?????i nh???n",
                            "zh-CN": "QA-????????????",
                            "zh-TW": "QA-????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "b317ff28-a237-4fb2-87f9-5274257a7f7c",
                        "parameterName": {
                            "en-US": "QA-Bank Account",
                            "hi-IN": "QA-???????????? ????????????",
                            "id-ID": "QA-Akun bank",
                            "ja-JP": "QA-????????????",
                            "ms-MY": "QA-Akaun bank",
                            "pt-BR": "QA-N??mero do cart??o banc??rio",
                            "th-TH": "QA-??????????????????????????????????????????",
                            "vi-VN": "QA-S??? t??i kho???n",
                            "zh-CN": "QA-????????????",
                            "zh-TW": "QA-????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "f2b77185-64c9-435c-92ef-c8ff9a36e216",
                        "parameterName": {
                            "en-US": "QA-Postscript",
                            "hi-IN": "QA-???????????????????????? ?????????",
                            "id-ID": "QA-Postscript",
                            "ja-JP": "QA-??????",
                            "ms-MY": "QA-Postscript",
                            "pt-BR": "QA-observa????o",
                            "th-TH": "QA-????????????????????????",
                            "vi-VN": "QA-N???i Dung Chuy???n ti???n",
                            "zh-CN": "QA-??????",
                            "zh-TW": "QA-??????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "QA-Please enter the postscript in the bank transfer remark field",
                            "hi-IN": "QA-??????????????? ???????????????????????? ????????????????????? ??????????????????????????? ??????????????? ??????????????? ??????????????????????????????",
                            "id-ID": "QA-Silahkan masukkan postscript di kolom komentar transfer bank",
                            "ja-JP": "QA-???????????????????????????????????????????????????????????????",
                            "ms-MY": "QA-Sila masukkan nota-nota dalam bidang pernyataan pemindahan bank",
                            "pt-BR": "QA-Certifique-se de colar a anota????o acima no campo de coment??rios / observa????o",
                            "th-TH": "QA-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????",
                            "vi-VN": "QA-Y??u C???u Nh???p ????ng Ghi Ch?? N??y Trong N???i Dung Chuy???n Kho???n Ng??n H??ng",
                            "zh-CN": "QA-??????????????????/??????????????????????????????",
                            "zh-TW": "QA-??????????????????/??????????????????????????????"
                        },
                        "otherSetting": {
                            "postscriptRule": "PLAYER_ID_ORIGINAL"
                        }
                    },
                    {
                        "parameterId": "54c25c91-5f79-44db-81bf-a495d9002e3f",
                        "parameterName": {
                            "en-US": "QA-Amount",
                            "hi-IN": "QA-Amount",
                            "id-ID": "QA-Jumlah",
                            "ja-JP": "QA-???",
                            "ms-MY": "QA-Jumlah",
                            "pt-BR": "QA-Valor do dep??sito",
                            "th-TH": "QA-?????????????????????????????????????????????",
                            "vi-VN": "QA-Nh???p s??? ti???n",
                            "zh-CN": "QA-????????????",
                            "zh-TW": "QA-????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "62ace749-9d2c-4395-9f84-1ad11fcb9d75",
                        "parameterName": {
                            "en-US": "QA-Depositor Name",
                            "hi-IN": "QA-???????????????????????? ?????? ?????????",
                            "id-ID": "QA-Nama Deposit",
                            "ja-JP": "QA-????????????",
                            "ms-MY": "QA-Nama Pendeposit",
                            "pt-BR": "QA-Nome do depositante",
                            "th-TH": "QA-???????????????????????????????????????????????????",
                            "vi-VN": "QA-H??? t??n ng?????i g???i",
                            "zh-CN": "QA-???????????????",
                            "zh-TW": "QA-???????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "QA-depositNameEnglish",
                            "hi-IN": "QA-depositName?????????",
                            "id-ID": "QA-depositNameIndonesia",
                            "ja-JP": "QA-depositName?????????",
                            "ms-MY": "QA-depositNameMelayu",
                            "pt-BR": "QA-depositNamePortugu??s",
                            "th-TH": "QA-depositName?????????",
                            "vi-VN": "QA-depositNameTi???ng Vi???t",
                            "zh-CN": "QA-depositName????????????",
                            "zh-TW": "QA-depositName????????????"
                        },
                        "otherSetting": None
                    },
                    {
                        "parameterId": "57df45f2-c5af-4257-9c63-03e395a80847",
                        "parameterName": {
                            "en-US": "QA-Remarks",
                            "hi-IN": "QA-Remarks",
                            "id-ID": "QA-Remarks",
                            "ja-JP": "QA-Remarks",
                            "ms-MY": "QA-Remarks",
                            "pt-BR": "QA-Remarks",
                            "th-TH": "QA-???????????????????????????",
                            "vi-VN": "QA-Nh???n x??t",
                            "zh-CN": "QA-????????????",
                            "zh-TW": "QA-????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "QA-remarksEnglish ",
                            "hi-IN": "QA-remarks?????????",
                            "id-ID": "QA-remarksIndonesia",
                            "ja-JP": "QA-remarks?????????",
                            "ms-MY": "QA-remarksMelayu",
                            "pt-BR": "QA-remarksPortugu??s",
                            "th-TH": "QA-remarks?????????",
                            "vi-VN": "QA-remarksTi???ng Vi???t",
                            "zh-CN": "QA-remarks???????????? ",
                            "zh-TW": "QA-remarks????????????"
                        },
                        "otherSetting": None
                    },
                    {
                        "parameterId": "1e91c311-1ee8-4a77-be33-65bf5ff18e3e",
                        "parameterName": {
                            "en-US": "QA-Upload Deposit Proof",
                            "hi-IN": "QA-?????????????????? ??????????????? ????????????",
                            "id-ID": "QA-Unduh Struk Pembayaran",
                            "ja-JP": "QA-??????????????????",
                            "ms-MY": "QA-Muat naik payslip",
                            "pt-BR": "QA-Carregar captura de tela",
                            "th-TH": "QA-???????????????????????????????????????????????????",
                            "vi-VN": "QA-T???i h??a ????n",
                            "zh-CN": "QA-????????????",
                            "zh-TW": "QA-????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "d1e005a3-7e0f-4cb9-8d13-e9da83fcd593",
                        "parameterName": {
                            "en-US": "Reminder",
                            "hi-IN": "Reminder",
                            "id-ID": "Reminder",
                            "ja-JP": "Reminder",
                            "ms-MY": "Reminder",
                            "pt-BR": "Reminder",
                            "th-TH": "?????????????????????????????????",
                            "vi-VN": "L??u ??",
                            "zh-CN": "????????????",
                            "zh-TW": "bankId"
                        },
                        "ecEnable": True,
                        "parameterRequired": False,
                        "parameterTips": {
                            "en-US": "QA-reminder????????????",
                            "hi-IN": "QA-reminder?????????",
                            "id-ID": "QA-reminderIndonesia",
                            "ja-JP": "QA-reminder?????????",
                            "ms-MY": "QA-reminderMelayu",
                            "pt-BR": "QA-reminderPortugu??s",
                            "th-TH": "QA-reminder?????????",
                            "vi-VN": "QA-reminderTi???ng Vi???t",
                            "zh-CN": "QA-reminder????????????",
                            "zh-TW": "QA-reminder????????????"
                        },
                        "otherSetting": None
                    }
                ]
            }
        elif deposit_method == 'netbank':
            method_id = '49ae3109-09d6-4eb2-975e-3830e3130a5e'
            payload = {
                "templates": [
                    {
                        "parameterId": "fb5c03ae-04f4-4003-bc62-f1a241eadb47",
                        "parameterName": {
                            "en-US": "Beneficiary Name",
                            "hi-IN": "QA-???????????????????????? ?????? ?????????",
                            "id-ID": "QA-Nama Penerima",
                            "ja-JP": "QA-????????????",
                            "ms-MY": "QA-Nama Penerima",
                            "pt-BR": "QA-Nome do beneficiado",
                            "th-TH": "QA-???????????????????????????????????????",
                            "vi-VN": "QA-Ch??? t??i kho???n",
                            "zh-CN": "????????????",
                            "zh-TW": "????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "ea6fc3c4-2f44-4dc6-bd85-907c93080cb7",
                        "parameterName": {
                            "en-US": "Bank Account",
                            "hi-IN": "QA-???????????? ????????????",
                            "id-ID": "QA-Akun bank",
                            "ja-JP": "QA-????????????",
                            "ms-MY": "QA-Akaun bank",
                            "pt-BR": "QA-N??mero do cart??o banc??rio",
                            "th-TH": "QA-??????????????????????????????????????????",
                            "vi-VN": "QA-S??? t??i kho???n",
                            "zh-CN": "????????????",
                            "zh-TW": "????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "c96e95a0-9f8c-43f2-bd8c-6038bda5fe2f",
                        "parameterName": {
                            "en-US": "Branch",
                            "hi-IN": "QA-??????????????????",
                            "id-ID": "QA-Cabang",
                            "ja-JP": "QA-??????",
                            "ms-MY": "QA-Cawangan",
                            "pt-BR": "QA-Nome da agencia",
                            "th-TH": "QA-????????????????????????",
                            "vi-VN": "QA-Chi nh??nh",
                            "zh-CN": "??????",
                            "zh-TW": "??????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "3ae43567-430e-4637-8f10-26599171ea5e",
                        "parameterName": {
                            "en-US": "IFSC Code",
                            "hi-IN": "QA-IFSC Code",
                            "id-ID": "QA-IFSC Code",
                            "ja-JP": "QA-IFSC Code",
                            "ms-MY": "QA-IFSC Code",
                            "pt-BR": "QA-IFSC Code",
                            "th-TH": "QA-IFSC Code",
                            "vi-VN": "QA-IFSC Code",
                            "zh-CN": "IFSC Code",
                            "zh-TW": "QA-IFSC Code"
                        },
                        "ecEnable": True,
                        "parameterRequired": False,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "9f0e2a2b-2657-4a20-b4db-519740467b0a",
                        "parameterName": {
                            "en-US": "Postscript",
                            "hi-IN": "QA-???????????????????????? ?????????",
                            "id-ID": "QA-Postscript",
                            "ja-JP": "QA-??????",
                            "ms-MY": "QA-Postscript",
                            "pt-BR": "QA-observa????o",
                            "th-TH": "QA-????????????????????????",
                            "vi-VN": "QA-N???i Dung Chuy???n ti???n",
                            "zh-CN": "??????",
                            "zh-TW": "??????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "Please enter the postscript in the bank transfer remark field",
                            "hi-IN": "QA-??????????????? ???????????????????????? ????????????????????? ??????????????????????????? ??????????????? ??????????????? ??????????????????????????????",
                            "id-ID": "QA-Silahkan masukkan postscript di kolom komentar transfer bank",
                            "ja-JP": "QA-???????????????????????????????????????????????????????????????",
                            "ms-MY": "QA-Sila masukkan nota-nota dalam bidang pernyataan pemindahan bank",
                            "pt-BR": "QA-Certifique-se de colar a anota????o acima no campo de coment??rios / observa????o",
                            "th-TH": "QA-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????",
                            "vi-VN": "QA-Y??u C???u Nh???p ????ng Ghi Ch?? N??y Trong N???i Dung Chuy???n Kho???n Ng??n H??ng",
                            "zh-CN": "??????????????????/??????????????????????????????",
                            "zh-TW": "QA-??????????????????/??????????????????????????????"
                        },
                        "otherSetting": {
                            "postscriptRule": "PLAYER_ID_RANDOM"
                        }
                    },
                    {
                        "parameterId": "166484dc-4fa0-4656-97ea-52eaea607b63",
                        "parameterName": {
                            "en-US": "Amount",
                            "hi-IN": "QA-Amount",
                            "id-ID": "QA-Jumlah",
                            "ja-JP": "QA-???",
                            "ms-MY": "QA-Jumlah",
                            "pt-BR": "QA-Valor do dep??sito",
                            "th-TH": "QA-?????????????????????????????????????????????",
                            "vi-VN": "QA-Nh???p s??? ti???n",
                            "zh-CN": "????????????",
                            "zh-TW": "????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "ec37e44f-ccc7-4f0f-bfc7-f8fcfe27df3f",
                        "parameterName": {
                            "en-US": "Depositor Name",
                            "hi-IN": "QA -???????????????????????? ?????? ?????????",
                            "id-ID": "QA -Nama Deposit",
                            "ja-JP": "QA -????????????",
                            "ms-MY": "QA -Nama Pendeposit",
                            "pt-BR": "QA -Nome do depositante",
                            "th-TH": "QA -???????????????????????????????????????????????????",
                            "vi-VN": "QA -H??? t??n ng?????i g???i",
                            "zh-CN": "???????????????",
                            "zh-TW": "???????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "Please enter your name",
                            "hi-IN": "QA-depositName?????????",
                            "id-ID": "QA-depositNameIndonesia",
                            "ja-JP": "QA-depositName?????????",
                            "ms-MY": "QA-depositName?????????",
                            "pt-BR": "QA-depositNamePortugu??s",
                            "th-TH": "QA-depositName?????????",
                            "vi-VN": "QA-depositNameTi???ng Vi???t",
                            "zh-CN": "QA-depositName????????????",
                            "zh-TW": "QA-depositName????????????"
                        },
                        "otherSetting": None
                    },
                    {
                        "parameterId": "08b8a2b4-1248-4b67-99a5-56cc8092b169",
                        "parameterName": {
                            "en-US": "Transfer from",
                            "hi-IN": "QA-Transfer from",
                            "id-ID": "QA-Transfer Dari",
                            "ja-JP": "QA-?????????",
                            "ms-MY": "QA-Pemindahan dari",
                            "pt-BR": "QA-banco de origem",
                            "th-TH": "QA-????????????????????????????????????",
                            "vi-VN": "QA-Ng??n h??ng chuy???n",
                            "zh-CN": "????????????",
                            "zh-TW": "????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "Please select",
                            "hi-IN": "QA-??????????????? ??????????????????",
                            "id-ID": "QA-Silahkan pilih",
                            "ja-JP": "QA-????????????????????????",
                            "ms-MY": "QA-Sila pilih",
                            "pt-BR": "QA-favor selecione",
                            "th-TH": "QA-???????????????????????????",
                            "vi-VN": "QA-Ch???n ng??n h??ng",
                            "zh-CN": "?????????",
                            "zh-TW": "QA-?????????"
                        },
                        "otherSetting": None
                    },
                    {
                        "parameterId": "537b7233-0505-42a8-b002-f6ae9ce33efe",
                        "parameterName": {
                            "en-US": "Remarks",
                            "hi-IN": "QA-Remarks",
                            "id-ID": "QA-Remarks",
                            "ja-JP": "QA-Remarks",
                            "ms-MY": "QA-Remarks",
                            "pt-BR": "QA-Remarks",
                            "th-TH": "QA-???????????????????????????",
                            "vi-VN": "QA-Nh???n x??t",
                            "zh-CN": "????????????",
                            "zh-TW": "????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "Please enter your note",
                            "hi-IN": "QA-remarks?????????",
                            "id-ID": "QA-remarksIndonesia",
                            "ja-JP": "QA-remarks?????????",
                            "ms-MY": "QA-remarksMelayu",
                            "pt-BR": "QA-remarksPortugu??s",
                            "th-TH": "QA-remarks?????????",
                            "vi-VN": "QA-remarksTi???ng Vi???t",
                            "zh-CN": "QA-remarks????????????",
                            "zh-TW": "QA-remarks????????????"
                        },
                        "otherSetting": None
                    },
                    {
                        "parameterId": "2b381f38-d246-43d1-8914-3b3af69c5285",
                        "parameterName": {
                            "en-US": "Upload Deposit Proof",
                            "hi-IN": "QA-?????????????????? ??????????????? ????????????",
                            "id-ID": "QA-Unduh Struk Pembayaran",
                            "ja-JP": "QA-??????????????????",
                            "ms-MY": "QA-Muat naik payslip",
                            "pt-BR": "QA-Carregar captura de tela",
                            "th-TH": "QA-???????????????????????????????????????????????????",
                            "vi-VN": "QA-T???i h??a ????n",
                            "zh-CN": "????????????",
                            "zh-TW": "????????????"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": None,
                        "otherSetting": None
                    },
                    {
                        "parameterId": "6d0e1f3a-a2ec-4445-a48d-a51b49e37cc0",
                        "parameterName": {
                            "en-US": "Reminder",
                            "hi-IN": "Reminder",
                            "id-ID": "Reminder",
                            "ja-JP": "Reminder",
                            "ms-MY": "Reminder",
                            "pt-BR": "Reminder",
                            "th-TH": "?????????????????????????????????",
                            "vi-VN": "L??u ??",
                            "zh-CN": "????????????",
                            "zh-TW": "bankId"
                        },
                        "ecEnable": True,
                        "parameterRequired": False,
                        "parameterTips": {
                            "en-US": "Say something you want to highlight",
                            "hi-IN": "QA-reminder?????????1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345",
                            "id-ID": "QA-reminderIndonesia1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345",
                            "ja-JP": "QA-reminder?????????1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345",
                            "ms-MY": "QA-reminderMelayu1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345",
                            "pt-BR": "QA-reminderPortugu??s1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345",
                            "th-TH": "QA-reminder?????????1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345",
                            "vi-VN": "QA-reminderTi???ng Vi???t1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345",
                            "zh-CN": "??????????????????????????????????????????????????????",
                            "zh-TW": "QA-reminder????????????1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345"
                        },
                        "otherSetting": None
                    }
                ]
            }

        _, token = self.ims_login()

        url = self.paymentInfo + f'/{method_id}'
        headers = {
            'content-type': 'application/json;charset=UTF-8',
            'accept-encoding': 'accept-encoding: gzip, deflate, br',
            'authorization': token['token']
        }

        r = self.s.put(url, headers=headers, json=payload)

        log(f"Set up deposit page setting: {r.status_code}")

    @allure.step('IMS ??????????????????')
    def deposit_audit_search(self, playerid):
        import time

        month = time.strftime('%m')
        day = time.strftime('%d')
        todays_start, todays_end = self.start_and_end_time(
            start_m=month,
            start_d=day,
            end_m=month,
            end_d=day
        )

        _, token = self.ims_login()

        url = self.deposit_audit
        headers = {
            'authorization': token['token']
        }
        params = {
            'playerid': playerid,
            'exactmatch': True,
            'depositPaymentTypeEnum': 'COMPANY_DEPOSIT',
            'endtime': todays_end,
            'language': 2,
            'limit': 25,
            'offset': 0,
            'sort': 'DESC',
            'sortcolumn': 'deposittime',
            'starttime': todays_start,
            'statusType': 'DEPOSIT_AUDIT',
            'timefilter': 'deposittime',
        }
        r = self.s.get(url, headers=headers, params=params)
        log(r.text)
        return r.json()

    @allure.step('IMS ??????????????????')
    def deposit_data_lock_or_not(self, deposit_id, status='unlock'):
        """status: 2 = ??????"""
        _, token = self.ims_login()
        url = f'{self.base}deposits/{deposit_id}/lock'

        headers = {
            'content-type': 'application/json;charset=UTF-8',
            'accept-encoding': 'accept-encoding: gzip, deflate, br',
            'authorization': token['token']
        }
        if status == 'unlock':
            status = 2
        elif status == 'lock':
            status = 1

        payload = {'status': status}
        r = self.s.put(url, headers=headers, json=payload)
        log(f'Deposit data lock or not: {r.status_code}')
        return r.status_code

    @allure.step('IMS ????????????, ??????')
    def deposit_data_approve(self, deposit_id, ec_remarks):
        """ ec_remarks: ???????????????"""
        _, token = self.ims_login()
        url = f'{self.base}deposits/{deposit_id}/approve'
        headers = {
            'content-type': 'application/json;charset=UTF-8',
            'accept-encoding': 'accept-encoding: gzip, deflate, br',
            'authorization': token['token']
        }
        payload = {'approvereason': "", 'ecremarks': ec_remarks}
        r = self.s.put(url, headers=headers, json=payload)
        log(f'Deposit data approve: {r.status_code}')
        return r.status_code

    @allure.step('IMS ??????, ??????, ????????????????????????')
    def bankcard(self, playerid, limit=10, method='get', payment_id=None):
        _, token = self.ims_login()

        headers = {
            'authorization': token['token']
        }
        params = {
            'playerid': playerid,
            'limit': limit,
            'sortcolumn': 'createdate',
            'sort': 'DESC',
            'language': 2
        }

        url = self.player_payments

        if method == 'delete':
            url = self.player_payments + f'/{payment_id}'
            r = self.s.delete(url, headers=headers)
            log(f'Bankcard delete: {r.status_code}')

            if r.status_code != 204:
                raise ValueError('Delete bankcard failed')

        elif method == 'get':
            r = self.s.get(url, headers=headers, params=params)

            log(f'Bankcard: {r.text}')
            # {'total' 3, 'data': [{'paymentid': 'asodiahwo', 'bankaccount': 111222},
            #                       {'paymentid'}, {}]}
            return r.json()
        elif method == 'post':
            # TODO: bankid ??????????????????, ?????????
            headers['content-type'] = 'multipart/form-data; boundary=----WebKitFormBoundaryciLEHEpAuAHzquF3'

            r = self.s.post(url, headers=headers, )

    @allure.step('IMS ??????????????????')
    def withdraw_audit_search(self, playerid):
        import time

        month = time.strftime('%m')
        day = time.strftime('%d')
        todays_start, todays_end = self.start_and_end_time(
            start_m=month,
            start_d=day,
            end_m=month,
            end_d=day
        )

        _, token = self.ims_login()

        url = self.withdraw_audit
        headers = {
            'authorization': token['token']
        }
        params = {
            'playerid': playerid,
            'exactmatch': True,
            'dl': False,
            'endtime': todays_end,
            'language': 2,
            'limit': 25,
            'offset': 0,
            'sequence': 0,
            'sort': 'DESC',
            'sortcolumn': 'withdrawaltime',
            'starttime': todays_start,
            'statusType': 'WITHDRAWAL_AUDIT',
            'timefilter': 'withdrawaltime',
        }
        r = self.s.get(url, headers=headers, params=params)
        log(r.text)
        return r.json()

    @allure.step('IMS ??????, ??????, ????????????????????????')
    def withdraw_datas_action(self, withdraw_id, status='unlock', finance=False):
        """
        ??????????????? reject ??????????????????, ????????????????????? unlock > approve
        """

        _, token = self.ims_login()
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': token['token'],
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://ae-bo.stgdevops.site',
            'referer': 'https://ae-bo.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/87.0.4280.88 Safari/537.36'
        }
        if status == 'unlock':
            url = f'{self.base}withdrawals/{withdraw_id}/lock'
            if finance is False:
                # ????????????
                payload = {'status': 5}
            else:
                # ????????????
                payload = {'status': 7}

            r = self.s.put(url, headers=headers, json=payload)
            log(f'Withdraw data unlock: {r.status_code}')
        elif status == 'reject':
            url = f'{self.base}withdrawals/{withdraw_id}/reject'
            payload = {'status': 12, 'declinereason': 'qq', 'ecremarks': 'qq'}
            r = self.s.put(url, headers=headers, json=payload)

            log(f'Withdraw data reject: {r.status_code}')
        elif status == 'approve':
            url = f'{self.base}withdrawals/{withdraw_id}/approve'
            if finance is False:
                # ????????????
                payload = {'status': 6, 'thirdpartypaymentid': None}
                r = self.s.put(url, headers=headers, json=payload)
                log(f'Withdraw data approve risk audit: {r.status_code}')
            else:
                # ????????????
                payload = {
                    'status': 8,
                    'approvereason': '',
                    'caccountid': '',
                    'ecremarks': 'qq',
                    'payoutwalletkey': None,
                    'thirdpartypaymentid': ''
                }
                r = self.s.put(url, headers=headers, json=payload)
                log(f'Withdraw data approve finance audit: {r.status_code}')



    @allure.step('Get timestamp')
    def start_and_end_time(
            self, start_m,
            start_d,
            end_m,
            end_d
    ):
        todays_start = ''
        todays_end = ''
        strftimes = (time.strftime('%Y') + f'-{start_m}-{start_d} 00:00:00',
                     time.strftime('%Y') + f'-{end_m}-{end_d} 23:59:59')

        for strftime in strftimes:
            strptime = time.strptime(strftime, '%Y-%m-%d %H:%M:%S')
            if strftime == strftimes[0]:
                todays_start = time.mktime(strptime)
            else:
                todays_end = time.mktime(strptime)

        return str(int(todays_start)) + '000', str(int(todays_end)) + '999'
