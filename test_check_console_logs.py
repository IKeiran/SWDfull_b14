import time
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@pytest.fixture(scope="session")
def setup_environment():
    global driver
    capabilities = DesiredCapabilities.CHROME
    capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}
    driver = Chrome(desired_capabilities=capabilities)

    # load the desired webpage
    driver.implicitly_wait(3)
    yield
    driver.close()


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


def login(driver):
    base_url = 'http://192.168.64.2/litecart/admin/'
    driver.get(base_url)

    login_page = LoginPage(driver)
    login_page.set_login('admin')
    login_page.set_password('admin')
    login_page.login_btn_click()


def fill_value(name, value):
    driver.find_element_by_name(name).clear()
    driver.find_element_by_name(name).send_keys(value)


def test_create_product(setup_environment):
    base_url = 'http://192.168.64.2/litecart/admin/'
    driver.get(base_url)
    login(driver)
    catalog_page_link = 'http://192.168.64.2/litecart/admin/?app=catalog&doc=catalog'
    driver.get(catalog_page_link)

    rows = driver.find_elements_by_xpath("//table[@class='dataTable']/*/tr[@class='row']/*/a")
    for index in range(0, len(rows), 2):
        driver.find_elements_by_xpath("//table[@class='dataTable']/*/tr[@class='row']/*/a")[index].click()
        time.sleep(1)
        assert 0 == len(driver.get_log('browser')), f"Browser console logs appears: driver.get_log('browser')"
        driver.back()
