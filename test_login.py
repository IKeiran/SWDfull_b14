import time

import pytest
from selenium.webdriver import Chrome


@pytest.fixture()
def setup_environment():
    global driver
    driver_path = '/Users/keiran/Downloads/chromedriver'
    driver = Chrome(executable_path=driver_path)
    driver.implicitly_wait(3)
    yield
    time.sleep(10)
    driver.close()


def test_login(setup_environment):
    base_url = 'http://192.168.64.2/litecart/admin/'
    driver.get(base_url)

    login_page = LoginPage(driver)
    login_page.set_login('admin')
    login_page.set_password('admin')
    login_page.login_btn_click()



class LoginPage:

    def __init__(self, driver):
        self.driver = driver

    def set_login(self, user_login):
        txt_username_name = 'username'
        self.driver.find_element_by_name(txt_username_name).clear()
        self.driver.find_element_by_name(txt_username_name).send_keys(user_login)

    def set_password(self, user_password):
        txt_userpassword_name = 'password'
        self.driver.find_element_by_name(txt_userpassword_name).clear()
        self.driver.find_element_by_name(txt_userpassword_name).send_keys(user_password)

    def login_btn_click(self):
        btn_login_name = 'login'
        self.driver.find_element_by_name(btn_login_name).click()
