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

log = lambda input_: logger.info(str(input_))


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

    @allure.step('使用 android 返回鍵')
    def android_go_back(self):
        self.driver.back()


class Ims:
    import requests

    s = requests.session()

    def __init__(self, env='stg'):
        self.base = f'https://ae-boapi.{env}devops.site/ae-ims/api/v1/'

        self.login = self.base + 'login'
        self.paymentInfo = self.base + 'deposits/setting/paymentInfoTemplate'
        self.deposit_audit = self.base + 'deposits/search'

    @allure.step('IMS 登入')
    def ims_login(self):
        url = self.login

        username = 'wellytest'
        pwd = 'dc18f76e9b59a3f84eb453cba8c2749d3e6b1eeb'

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

    @allure.step('IMS 設定存款頁面設定')
    def set_up_deposit_page_settings(self, deposit_method='offline'):
        """
        payload 裡的 templates 我目前設定的是 線下入款, 必填的只有"存款人姓名"跟"轉出銀行",
        調適完確定了上傳截圖再去抓都開的 api
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
                            "hi-IN": "QA-लाभार्थी का नाम",
                            "id-ID": "QA-Nama Penerima",
                            "ja-JP": "QA-受取人名",
                            "ms-MY": "QA-Beneficiary Name",
                            "pt-BR": "QA-Nome do beneficiado",
                            "th-TH": "QA-ชื่อผู้รับโอน",
                            "vi-VN": "QA-Chủ tài khoản",
                            "zh-CN": "收款姓名",
                            "zh-TW": "收款姓名"
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
                            "hi-IN": "QA-बैंक खाता",
                            "id-ID": "QA-Akun bank",
                            "ja-JP": "QA-銀行口座",
                            "ms-MY": "QA-Bank Account",
                            "pt-BR": "QA-Número do cartão bancário",
                            "th-TH": "QA-เลขบัญชีธนาคาร",
                            "vi-VN": "QA-Số tài khoản",
                            "zh-CN": "收款卡号",
                            "zh-TW": "收款卡號"
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
                            "hi-IN": "QA-ब्रांच",
                            "id-ID": "QA-Cabang",
                            "ja-JP": "QA-支店",
                            "ms-MY": "QA-Branch",
                            "pt-BR": "QA-Nome da agencia",
                            "th-TH": "QA-ชื่อสาขา",
                            "vi-VN": "QA-Chi nhánh",
                            "zh-CN": "支行",
                            "zh-TW": "支行"
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
                            "hi-IN": "QA-परिशिष्ट भाग",
                            "id-ID": "QA-Postscript",
                            "ja-JP": "QA-追記",
                            "ms-MY": "QA-Postscript",
                            "pt-BR": "QA-observação",
                            "th-TH": "QA-คำลงท้าย",
                            "vi-VN": "QA-Nội Dung Chuyển tiền",
                            "zh-CN": "附言",
                            "zh-TW": "附言"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "Please enter the postscript in the bank transfer remark field",
                            "hi-IN": "QA-வங்கி பரிமாற்ற கருத்து புலத்தில் தபால் பதிவை உள்ளிடவும்",
                            "id-ID": "QA-Silahkan masukkan postscript di kolom komentar transfer bank",
                            "ja-JP": "QA-銀行振込の備考欄に追記を入力してください。",
                            "ms-MY": "QA-Sila masukkan nota-nota dalam bidang pernyataan pemindahan bank",
                            "pt-BR": "QA-Certifique-se de colar a anotação acima no campo de comentários / observação",
                            "th-TH": "QA-โปรดใส่คำลงท้ายลงบนช่องหมายเหตุการโอนเงินธนาคาร",
                            "vi-VN": "QA-Yêu Cầu Nhập Đúng Ghi Chú Này Trong Nội Dung Chuyển Khoản Ngân Hàng",
                            "zh-CN": "请务必在备注/附言等处贴上以上附言",
                            "zh-TW": "QA-請務必在備註/附言等處貼上以上附言"
                        },
                        "otherSetting": {
                            "postscriptRule": "PLAYER_ID_ORIGINAL"
                        }
                    },
                    {
                        "parameterId": "23095923-c372-4732-9128-d037d32bbf49",
                        "parameterName": {
                            "en-US": "Deposit Method",
                            "hi-IN": "QA-जमा प्रकार",
                            "id-ID": "QA-Tipe Deposit",
                            "ja-JP": "QA-入金タイプ",
                            "ms-MY": "QA-Deposit Method",
                            "pt-BR": "QA-forma de depósito",
                            "th-TH": "QA-วิธีการฝากเงิน",
                            "vi-VN": "QA-Phương thức nạp",
                            "zh-CN": "存款方式",
                            "zh-TW": "存款方式"
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
                            "ja-JP": "QA-額",
                            "ms-MY": "QA-Amount",
                            "pt-BR": "QA-Valor do depósito",
                            "th-TH": "QA-จำนวนเงินที่ฝาก",
                            "vi-VN": "QA-Nhập số tiền",
                            "zh-CN": "存款金额",
                            "zh-TW": "存款金額"
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
                            "hi-IN": "QA-जमा समय",
                            "id-ID": "QA-Waktu Deposit",
                            "ja-JP": "QA-入金時間",
                            "ms-MY": "QA-Deposit Time",
                            "pt-BR": "QA-Horário do depósito",
                            "th-TH": "QA-เวลาฝากเงิน",
                            "vi-VN": "QA-Thời gian gửi",
                            "zh-CN": "存款时间",
                            "zh-TW": "存款時間"
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
                            "hi-IN": "QA-जमाकर्ता का नाम",
                            "id-ID": "QA-Nama Deposit",
                            "ja-JP": "QA-入金者名",
                            "ms-MY": "QA-Depositor Name",
                            "pt-BR": "QA-Nome do depositante",
                            "th-TH": "QA-ชื่อของผู้ฝากเงิน",
                            "vi-VN": "QA-Họ tên người gửi",
                            "zh-CN": "存款人姓名",
                            "zh-TW": "存款人姓名"
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
                            "vi-VN": "Tiếng Việt Tiếng Việt",
                            "zh-CN": "QA-depositName簡體中文",
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
                            "ja-JP": "QA-送金元",
                            "ms-MY": "QA-Transfer from",
                            "pt-BR": "QA-banco de origem",
                            "th-TH": "QA-โอนจากธนาคาร",
                            "vi-VN": "QA-Ngân hàng chuyển",
                            "zh-CN": "转出银行",
                            "zh-TW": "轉出銀行"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "Please select",
                            "hi-IN": "QA-कृपया चुनें।",
                            "id-ID": "QA-Silahkan pilih",
                            "ja-JP": "QA-選択してください",
                            "ms-MY": "QA-Sila pilih",
                            "pt-BR": "QA-favor selecione",
                            "th-TH": "QA-โปรดเลือก",
                            "vi-VN": "QA-Chọn ngân hàng",
                            "zh-CN": "请选择",
                            "zh-TW": "QA-請選擇"
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
                            "th-TH": "QA-ข้อสังเกต",
                            "vi-VN": "QA-Nhận xét",
                            "zh-CN": "存款备注",
                            "zh-TW": "存款備註"
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
                            "zh-CN": "QA-remarks簡體中文",
                            "zh-TW": ""
                        },
                        "otherSetting": None
                    },
                    {
                        "parameterId": "9cae777a-ad76-4fe0-8b79-6ba3a4633350",
                        "parameterName": {
                            "en-US": "Upload Deposit Proof",
                            "hi-IN": "QA-भुगतान अपलोड करें",
                            "id-ID": "QA-Unduh Struk Pembayaran",
                            "ja-JP": "QA-領収書の写真",
                            "ms-MY": "QA-Upload Deposit Proof",
                            "pt-BR": "QA-Carregar captura de tela",
                            "th-TH": "QA-อัพโหลดสลิปการโอน",
                            "vi-VN": "QA-Tải hóa đơn",
                            "zh-CN": "上传截图",
                            "zh-TW": "上傳截圖"
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
                            "th-TH": "เตือนความจำ",
                            "vi-VN": "Lưu ý",
                            "zh-CN": "注意事项",
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
                            "zh-CN": "请提交至正确收款帐户，以加速入款时间",
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
                            "hi-IN": "QA-खाता नाम",
                            "id-ID": "QA-Akun",
                            "ja-JP": "QA-アカウント",
                            "ms-MY": "QA-Nama akaun",
                            "pt-BR": "QA-Nome da conta",
                            "th-TH": "QA-บัญชี",
                            "vi-VN": "QA-Tên người nhận",
                            "zh-CN": "QA-账户名称",
                            "zh-TW": "QA-賬戶名稱"
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
                            "hi-IN": "QA-बैंक खाता",
                            "id-ID": "QA-Akun bank",
                            "ja-JP": "QA-銀行口座",
                            "ms-MY": "QA-Akaun bank",
                            "pt-BR": "QA-Número do cartão bancário",
                            "th-TH": "QA-เลขบัญชีธนาคาร",
                            "vi-VN": "QA-Số tài khoản",
                            "zh-CN": "QA-收款卡号",
                            "zh-TW": "QA-收款卡號"
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
                            "hi-IN": "QA-परिशिष्ट भाग",
                            "id-ID": "QA-Postscript",
                            "ja-JP": "QA-追記",
                            "ms-MY": "QA-Postscript",
                            "pt-BR": "QA-observação",
                            "th-TH": "QA-คำลงท้าย",
                            "vi-VN": "QA-Nội Dung Chuyển tiền",
                            "zh-CN": "QA-附言",
                            "zh-TW": "QA-附言"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "QA-Please enter the postscript in the bank transfer remark field",
                            "hi-IN": "QA-வங்கி பரிமாற்ற கருத்து புலத்தில் தபால் பதிவை உள்ளிடவும்",
                            "id-ID": "QA-Silahkan masukkan postscript di kolom komentar transfer bank",
                            "ja-JP": "QA-銀行振込の備考欄に追記を入力してください。",
                            "ms-MY": "QA-Sila masukkan nota-nota dalam bidang pernyataan pemindahan bank",
                            "pt-BR": "QA-Certifique-se de colar a anotação acima no campo de comentários / observação",
                            "th-TH": "QA-โปรดใส่คำลงท้ายลงบนช่องหมายเหตุการโอนเงินธนาคาร",
                            "vi-VN": "QA-Yêu Cầu Nhập Đúng Ghi Chú Này Trong Nội Dung Chuyển Khoản Ngân Hàng",
                            "zh-CN": "QA-请务必在备注/附言等处贴上以上附言",
                            "zh-TW": "QA-請務必在備註/附言等處貼上以上附言"
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
                            "ja-JP": "QA-額",
                            "ms-MY": "QA-Jumlah",
                            "pt-BR": "QA-Valor do depósito",
                            "th-TH": "QA-จำนวนเงินที่ฝาก",
                            "vi-VN": "QA-Nhập số tiền",
                            "zh-CN": "QA-存款金额",
                            "zh-TW": "QA-存款金額"
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
                            "hi-IN": "QA-जमाकर्ता का नाम",
                            "id-ID": "QA-Nama Deposit",
                            "ja-JP": "QA-入金者名",
                            "ms-MY": "QA-Nama Pendeposit",
                            "pt-BR": "QA-Nome do depositante",
                            "th-TH": "QA-ชื่อของผู้ฝากเงิน",
                            "vi-VN": "QA-Họ tên người gửi",
                            "zh-CN": "QA-存款人姓名",
                            "zh-TW": "QA-存款人姓名"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "QA-depositNameEnglish",
                            "hi-IN": "QA-depositName印度语",
                            "id-ID": "QA-depositNameIndonesia",
                            "ja-JP": "QA-depositName日本语",
                            "ms-MY": "QA-depositNameMelayu",
                            "pt-BR": "QA-depositNamePortuguês",
                            "th-TH": "QA-depositNameไทย",
                            "vi-VN": "QA-depositNameTiếng Việt",
                            "zh-CN": "QA-depositName简体中文",
                            "zh-TW": "QA-depositName繁體中文"
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
                            "th-TH": "QA-ข้อสังเกต",
                            "vi-VN": "QA-Nhận xét",
                            "zh-CN": "QA-存款备注",
                            "zh-TW": "QA-存款備註"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "QA-remarksEnglish ",
                            "hi-IN": "QA-remarks印度语",
                            "id-ID": "QA-remarksIndonesia",
                            "ja-JP": "QA-remarks日本语",
                            "ms-MY": "QA-remarksMelayu",
                            "pt-BR": "QA-remarksPortuguês",
                            "th-TH": "QA-remarksไทย",
                            "vi-VN": "QA-remarksTiếng Việt",
                            "zh-CN": "QA-remarks简体中文 ",
                            "zh-TW": "QA-remarks繁體中文"
                        },
                        "otherSetting": None
                    },
                    {
                        "parameterId": "1e91c311-1ee8-4a77-be33-65bf5ff18e3e",
                        "parameterName": {
                            "en-US": "QA-Upload Deposit Proof",
                            "hi-IN": "QA-भुगतान अपलोड करें",
                            "id-ID": "QA-Unduh Struk Pembayaran",
                            "ja-JP": "QA-領収書の写真",
                            "ms-MY": "QA-Muat naik payslip",
                            "pt-BR": "QA-Carregar captura de tela",
                            "th-TH": "QA-อัพโหลดสลิปการโอน",
                            "vi-VN": "QA-Tải hóa đơn",
                            "zh-CN": "QA-上传截图",
                            "zh-TW": "QA-上傳截圖"
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
                            "th-TH": "เตือนความจำ",
                            "vi-VN": "Lưu ý",
                            "zh-CN": "注意事项",
                            "zh-TW": "bankId"
                        },
                        "ecEnable": True,
                        "parameterRequired": False,
                        "parameterTips": {
                            "en-US": "QA-reminder简体中文",
                            "hi-IN": "QA-reminder印度语",
                            "id-ID": "QA-reminderIndonesia",
                            "ja-JP": "QA-reminder日本语",
                            "ms-MY": "QA-reminderMelayu",
                            "pt-BR": "QA-reminderPortuguês",
                            "th-TH": "QA-reminderไทย",
                            "vi-VN": "QA-reminderTiếng Việt",
                            "zh-CN": "QA-reminder简体中文",
                            "zh-TW": "QA-reminder繁體中文"
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
                            "hi-IN": "QA-लाभार्थी का नाम",
                            "id-ID": "QA-Nama Penerima",
                            "ja-JP": "QA-受取人名",
                            "ms-MY": "QA-Nama Penerima",
                            "pt-BR": "QA-Nome do beneficiado",
                            "th-TH": "QA-ชื่อผู้รับโอน",
                            "vi-VN": "QA-Chủ tài khoản",
                            "zh-CN": "收款姓名",
                            "zh-TW": "收款姓名"
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
                            "hi-IN": "QA-बैंक खाता",
                            "id-ID": "QA-Akun bank",
                            "ja-JP": "QA-銀行口座",
                            "ms-MY": "QA-Akaun bank",
                            "pt-BR": "QA-Número do cartão bancário",
                            "th-TH": "QA-เลขบัญชีธนาคาร",
                            "vi-VN": "QA-Số tài khoản",
                            "zh-CN": "收款卡号",
                            "zh-TW": "收款卡號"
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
                            "hi-IN": "QA-ब्रांच",
                            "id-ID": "QA-Cabang",
                            "ja-JP": "QA-支店",
                            "ms-MY": "QA-Cawangan",
                            "pt-BR": "QA-Nome da agencia",
                            "th-TH": "QA-ชื่อสาขา",
                            "vi-VN": "QA-Chi nhánh",
                            "zh-CN": "支行",
                            "zh-TW": "支行"
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
                            "hi-IN": "QA-परिशिष्ट भाग",
                            "id-ID": "QA-Postscript",
                            "ja-JP": "QA-追記",
                            "ms-MY": "QA-Postscript",
                            "pt-BR": "QA-observação",
                            "th-TH": "QA-คำลงท้าย",
                            "vi-VN": "QA-Nội Dung Chuyển tiền",
                            "zh-CN": "附言",
                            "zh-TW": "附言"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "Please enter the postscript in the bank transfer remark field",
                            "hi-IN": "QA-வங்கி பரிமாற்ற கருத்து புலத்தில் தபால் பதிவை உள்ளிடவும்",
                            "id-ID": "QA-Silahkan masukkan postscript di kolom komentar transfer bank",
                            "ja-JP": "QA-銀行振込の備考欄に追記を入力してください。",
                            "ms-MY": "QA-Sila masukkan nota-nota dalam bidang pernyataan pemindahan bank",
                            "pt-BR": "QA-Certifique-se de colar a anotação acima no campo de comentários / observação",
                            "th-TH": "QA-โปรดใส่คำลงท้ายลงบนช่องหมายเหตุการโอนเงินธนาคาร",
                            "vi-VN": "QA-Yêu Cầu Nhập Đúng Ghi Chú Này Trong Nội Dung Chuyển Khoản Ngân Hàng",
                            "zh-CN": "请务必在备注/附言等处贴上以上附言",
                            "zh-TW": "QA-請務必在備註/附言等處貼上以上附言"
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
                            "ja-JP": "QA-額",
                            "ms-MY": "QA-Jumlah",
                            "pt-BR": "QA-Valor do depósito",
                            "th-TH": "QA-จำนวนเงินที่ฝาก",
                            "vi-VN": "QA-Nhập số tiền",
                            "zh-CN": "存款金额",
                            "zh-TW": "存款金額"
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
                            "hi-IN": "QA -जमाकर्ता का नाम",
                            "id-ID": "QA -Nama Deposit",
                            "ja-JP": "QA -入金者名",
                            "ms-MY": "QA -Nama Pendeposit",
                            "pt-BR": "QA -Nome do depositante",
                            "th-TH": "QA -ชื่อของผู้ฝากเงิน",
                            "vi-VN": "QA -Họ tên người gửi",
                            "zh-CN": "存款人姓名",
                            "zh-TW": "存款人姓名"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "Please enter your name",
                            "hi-IN": "QA-depositName印度语",
                            "id-ID": "QA-depositNameIndonesia",
                            "ja-JP": "QA-depositName日本语",
                            "ms-MY": "QA-depositNameไทย",
                            "pt-BR": "QA-depositNamePortuguês",
                            "th-TH": "QA-depositNameไทย",
                            "vi-VN": "QA-depositNameTiếng Việt",
                            "zh-CN": "QA-depositName簡體中文",
                            "zh-TW": "QA-depositName繁體中文"
                        },
                        "otherSetting": None
                    },
                    {
                        "parameterId": "08b8a2b4-1248-4b67-99a5-56cc8092b169",
                        "parameterName": {
                            "en-US": "Transfer from",
                            "hi-IN": "QA-Transfer from",
                            "id-ID": "QA-Transfer Dari",
                            "ja-JP": "QA-送金元",
                            "ms-MY": "QA-Pemindahan dari",
                            "pt-BR": "QA-banco de origem",
                            "th-TH": "QA-โอนจากธนาคาร",
                            "vi-VN": "QA-Ngân hàng chuyển",
                            "zh-CN": "转出银行",
                            "zh-TW": "轉出銀行"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "Please select",
                            "hi-IN": "QA-कृपया चुनें।",
                            "id-ID": "QA-Silahkan pilih",
                            "ja-JP": "QA-選択してください",
                            "ms-MY": "QA-Sila pilih",
                            "pt-BR": "QA-favor selecione",
                            "th-TH": "QA-โปรดเลือก",
                            "vi-VN": "QA-Chọn ngân hàng",
                            "zh-CN": "请选择",
                            "zh-TW": "QA-請選擇"
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
                            "th-TH": "QA-ข้อสังเกต",
                            "vi-VN": "QA-Nhận xét",
                            "zh-CN": "存款备注",
                            "zh-TW": "存款備註"
                        },
                        "ecEnable": True,
                        "parameterRequired": True,
                        "parameterTips": {
                            "en-US": "Please enter your note",
                            "hi-IN": "QA-remarks印度语",
                            "id-ID": "QA-remarksIndonesia",
                            "ja-JP": "QA-remarks日本语",
                            "ms-MY": "QA-remarksMelayu",
                            "pt-BR": "QA-remarksPortuguês",
                            "th-TH": "QA-remarksไทย",
                            "vi-VN": "QA-remarksTiếng Việt",
                            "zh-CN": "QA-remarks簡體中文",
                            "zh-TW": "QA-remarks繁體中文"
                        },
                        "otherSetting": None
                    },
                    {
                        "parameterId": "2b381f38-d246-43d1-8914-3b3af69c5285",
                        "parameterName": {
                            "en-US": "Upload Deposit Proof",
                            "hi-IN": "QA-भुगतान अपलोड करें",
                            "id-ID": "QA-Unduh Struk Pembayaran",
                            "ja-JP": "QA-領収書の写真",
                            "ms-MY": "QA-Muat naik payslip",
                            "pt-BR": "QA-Carregar captura de tela",
                            "th-TH": "QA-อัพโหลดสลิปการโอน",
                            "vi-VN": "QA-Tải hóa đơn",
                            "zh-CN": "上传截图",
                            "zh-TW": "上傳截圖"
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
                            "th-TH": "เตือนความจำ",
                            "vi-VN": "Lưu ý",
                            "zh-CN": "注意事项",
                            "zh-TW": "bankId"
                        },
                        "ecEnable": True,
                        "parameterRequired": False,
                        "parameterTips": {
                            "en-US": "Say something you want to highlight",
                            "hi-IN": "QA-reminder印度语1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345",
                            "id-ID": "QA-reminderIndonesia1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345",
                            "ja-JP": "QA-reminder日本语1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345",
                            "ms-MY": "QA-reminderMelayu1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345",
                            "pt-BR": "QA-reminderPortuguês1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345",
                            "th-TH": "QA-reminderไทย1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345",
                            "vi-VN": "QA-reminderTiếng Việt1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345",
                            "zh-CN": "请提交至正确收款帐户，以加速入款时间",
                            "zh-TW": "QA-reminder繁體中文1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345"
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

    @allure.step('IMS 存款審核搜尋')
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

    @allure.step('IMS 審核單據解鎖')
    def deposit_data_lock_or_not(self, deposit_id, status='unlock'):
        """status: 2 = 解鎖"""
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

    @allure.step('IMS 通過審核, 給錢')
    def deposit_data_approve(self, deposit_id, ec_remarks):
        """ ec_remarks: 顯示再前端"""
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
