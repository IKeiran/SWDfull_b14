import time
import uuid
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.support.select import Select

import random


@pytest.fixture(scope="session")
def setup_environment():
    global driver
    driver = Chrome()
    driver.implicitly_wait(3)
    yield
    time.sleep(5)
    driver.close()


def fill_value(name, value):
    driver.find_element_by_name(name).clear()
    driver.find_element_by_name(name).send_keys(value)


def test_goods_creation(setup_environment):
    base_url = 'http://192.168.64.2/litecart/'
    driver.get(base_url)

    driver.find_element_by_link_text("New customers click here").click()

    time.sleep(3)
    # general tab
    email = f'test_{uuid.uuid1()}@gmail.com'
    password = 'test'
    fill_value("tax_id", "123456")
    fill_value("company", "HomeInc")
    fill_value("firstname", "test_user")
    fill_value("lastname", "test_user")
    fill_value("address1", "test_adddr1")
    fill_value("address2", "test_adddr2")
    fill_value("postcode", "98765")
    fill_value("city", "Odessa")
    fill_value("email", email)
    fill_value("phone", "+12345678")
    fill_value("password", password)
    fill_value("confirmed_password", password)

    country = "country_code"
    select = Select(driver.find_element_by_name(country))
    select.select_by_value("US")
    driver.find_element_by_name("create_account").click()

    time.sleep(1)
    fill_value("password", password)
    fill_value("confirmed_password", password)
    driver.find_element_by_name("create_account").click()

    # logout
    driver.find_element_by_link_text("Logout").click()

    # login
    time.sleep(2)
    fill_value("email", email)
    fill_value("password", password)
    driver.find_element_by_name("login").click()

    # logout
    time.sleep(20)
    driver.find_element_by_link_text("Logout").click()

    time.sleep(5)
