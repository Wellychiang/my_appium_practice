from selenium.webdriver.support.ui import WebDriverWait


class Base:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, args):
        try:
            WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element_by_xpath(args)).is_displayed()
            return self.driver.find_element_by_xpath(args)
        except:
            raise ValueError(f'Can not find {args} element')

    def find_id(self, args):
        try:
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_id(args)).is_displayed()
            return self.driver.find_element_by_id(args)
        except:
            raise ValueError(f'Can not find {args} element')

    def slide(self, direction, time=200):
        screen_size = self.driver.get_window_size(self)

        if direction == 'swipe left':
            x1 = screen_size['width'] * 0.75
            y1 = screen_size['height'] * 0.5
            x2 = screen_size['width'] * 0.25
            self.driver.swipe(x1, y1, x2, y1, time)



class Slide:

    def __init__(self, driver):
        self.driver = driver

    # 獲取螢幕大小
    def get_screen_size(self):
        return self.driver.get_window_size(self)

    # 上滑
    def swipe_up(self, t):
        screen_size = self.get_screen_size()
        x1 = screen_size['width'] * 0.5
        y1 = screen_size['height'] * 0.75
        y2 = screen_size['height'] * 0.25
        self.driver.swipe(x1, y1, x1, y2, t)

    # 下滑
    def swipe_down(self, t):
        screen_size = self.get_screen_size()
        x1 = screen_size['width'] * 0.5
        y1 = screen_size['height'] * 0.25
        y2 = screen_size['height'] * 0.75
        self.driver.swipe(x1, y1, x1, y2, t)

    # 左滑
    def swipe_left(self, t):
        screen_size = self.get_screen_size()
        x1 = screen_size['width'] * 0.75
        y1 = screen_size['height'] * 0.5
        x2 = screen_size['width'] * 0.25
        self.driver.swipe(x1, y1, x2, y1, t)

    # 右滑
    def swipe_right(self, t):
        screen_size = self.get_screen_size()
        x1 = screen_size['width'] * 0.25
        y1 = screen_size['height'] * 0.5
        x2 = screen_size['width'] * 0.75
        self.driver.swipe(x1, y1, x2, y1, t)