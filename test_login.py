import time

import pytest
from selenium.webdriver import Chrome
from Pages.adminLoginPage import AdminLoginPage

@pytest.fixture()
def setup_environment():
    global driver
    driver_path = '/Users/keiran/Downloads/chromedriver'
    driver = Chrome(executable_path=driver_path)
    driver.implicitly_wait(3)
    yield
    time.sleep(3)
    driver.close()


def test_login(setup_environment):
    base_url = 'http://192.168.64.2/litecart/admin/'
    driver.get(base_url)

    login_page = AdminLoginPage(driver)
    login_page.set_login('admin')
    login_page.set_password('admin')
    login_page.login_btn_click()




