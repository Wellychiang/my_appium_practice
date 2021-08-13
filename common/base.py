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

log = lambda input_:logger.info(str(input_))


class Base:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, args):
        try:
            WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_xpath(args)).is_displayed()
            return self.driver.find_element_by_xpath(args)
        except:
            self.get_screen_shot()
            log(f'Can not find {args} element')
            return False

    def find_id(self, args):
        try:
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_id(args)).is_displayed()
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
            if str_ == ' ' or str_ == '-' or str_ == ':':
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



