import time

import pytest
from selenium.webdriver import Chrome


class SingletonDriver():
    _instanse = None
    def __new__(self):
        if not self._instanse:
            self._instanse = super(SingletonDriver, self).__new__(self)
        return self._instanse


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


def test_sidebar_menu(setup_environment):
    base_url = 'http://192.168.64.2/litecart/admin/'
    menu_links = list()
    driver.get(base_url)
    login(driver)
    menu_block = driver.find_element_by_id("box-apps-menu")
    links = menu_block.find_elements_by_xpath(".//a")
    side_menu_item = 'li#app-'
    sel = "(//li[@id='app-'])"

    for link in links:
        menu_links.append(link.get_attribute('href'))

    for index, menu_link in enumerate(menu_links):
        driver.get(menu_link)
        title = driver.find_elements_by_tag_name('title')
        assert title

        sidebar = driver.find_elements_by_xpath(sel)[index]
        dlinks = sidebar.find_elements_by_css_selector("a")
        side_menu_sub_items = list()
        for link in dlinks:
            side_menu_sub_items.append(link.get_attribute('href'))
        for sub_item in side_menu_sub_items:
            driver.get(sub_item)

            title = driver.find_elements_by_tag_name('h1')
            assert title
        time.sleep(2)





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