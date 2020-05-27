import time

import pytest
from selenium.webdriver import Chrome


@pytest.fixture(scope="session")
def setup_environment():
    global driver
    driver = Chrome()
    driver.implicitly_wait(3)
    yield
    time.sleep(1)
    driver.close()


def login(driver):
    base_url = 'http://192.168.64.2/litecart/admin/'
    driver.get(base_url)

    login_page = LoginPage(driver)
    login_page.set_login('admin')
    login_page.set_password('admin')
    login_page.login_btn_click()


def test_external_links(setup_environment):
    base_url = 'http://192.168.64.2/litecart/admin/'
    driver.get(base_url)
    login(driver)
    countries_link = 'http://192.168.64.2/litecart/admin/?app=countries&doc=countries'
    driver.get(countries_link)

    driver.find_element_by_link_text("Add New Country").click()
    external_links = driver.find_elements_by_xpath("//tr/*/a[@target='_blank']")
    print(len(external_links))

    for link in external_links:
        link.click()
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])



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