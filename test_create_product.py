import time
import uuid
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.support.select import Select
import pathlib
import random


@pytest.fixture(scope="session")
def setup_environment():
    global driver
    driver = Chrome()
    driver.implicitly_wait(3)
    yield
    time.sleep(5)
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


def test_goods_creation(setup_environment):
    base_url = 'http://192.168.64.2/litecart/admin/'
    driver.get(base_url)
    login(driver)
    menu_block = driver.find_element_by_id("box-apps-menu")
    links = menu_block.find_elements_by_xpath(".//a")
    catalog_link = links[1].get_attribute('href')
    driver.get(catalog_link)
    catalog_page = driver.find_element_by_link_text("Add New Product").get_attribute('href')
    driver.get(catalog_page)

    # general tab
    enable = driver.find_element_by_xpath("(//input[@name='status'])[1]").click()
    item_name = f'test_{uuid.uuid1()}'
    print(item_name)
    fill_value("name[en]", item_name)
    fill_value("code", f'code_{item_name}')
    fill_value("quantity", random.randint(1, 100))

    # image
    filepath = "/Users/keiran/Downloads/photo_2018-08-31_22-30-38.jpg"
    filepath = '%s/data/Image1.jpg' % pathlib.Path(__file__).parent.absolute()
    driver.find_element_by_name("new_images[]").send_keys(filepath)
    # date
    fill_value("date_valid_from", "21122018")
    fill_value("date_valid_to", "21122024")

    # information tab
    driver.find_element_by_link_text("Information").click()
    fill_value("keywords", "first, second, third")
    fill_value("short_description[en]", f'Short description for item {item_name}')

    description_css = '.trumbowyg-editor'
    driver.find_element_by_css_selector(description_css).send_keys(f'Full description for item {item_name}')

    fill_value("head_title[en]", "Head title for item {item_name}")
    fill_value("meta_description[en]", "Meta desk for item  {item_name}")

    # prices tab
    driver.find_element_by_link_text("Prices").click()

    purchase_price = "purchase_price"
    income_price = round(10 * random.random(), 2)
    price = str(income_price)
    fill_value("purchase_price", price)

    currency = "purchase_price_currency_code"
    select = Select(driver.find_element_by_name(currency))
    select.select_by_index(1)

    fill_value("prices[USD]", str(2 * income_price))
    fill_value("gross_prices[USD]", str(2 * income_price))
    fill_value("prices[EUR]", str(2 * income_price))
    fill_value("gross_prices[EUR]", str(2 * income_price))

    # submit
    driver.find_element_by_name("save").click()

    table = driver.find_element_by_class_name("dataTable")
    rows = table.find_elements_by_class_name("row")
    items = list()
    for row in rows[1:]:
        items.append(row.find_elements_by_tag_name('td')[2].text)

    assert item_name in items, f"Item {item_name}not found!"
