import time
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture(scope="session")
def setup_environment():
    global driver
    driver = Chrome()
    driver.implicitly_wait(3)
    yield
    time.sleep(5)
    driver.close()


def get_items_quantity():
    items_quantity_xpath = "//span[@class='quantity']"
    return int(driver.find_element_by_xpath(items_quantity_xpath).text)


def get_items_count_from_table():
    table_xpath = "//table[@class='dataTable rounded-corners']/*/tr/td[@class='item']/.."
    items = driver.find_elements_by_xpath(table_xpath)
    items_count = 0
    for item in items:
        data = item.find_elements_by_xpath('.//td')[0]
        items_count += int(data.text)
    return items_count


def remove_item_from_basket():
    remove_xpath = "//button[@name='remove_cart_item']"
    driver.find_element_by_xpath(remove_xpath).click()
    driver.refresh()


def test_shopping_card(setup_environment):
    base_url = 'https://litecart.stqa.ru/en/'
    driver.get(base_url)
    product_xpath = "//li[@class='product column shadow hover-light']"
    count = get_items_quantity()

    add_button_xpath = "//button[@name='add_cart_product']"

    # fill shopping card by products
    max_items = 3
    for _ in range(max_items):
        driver.find_elements_by_xpath(product_xpath)[0].click()
        driver.find_element_by_xpath(add_button_xpath).click()
        new_count = get_items_quantity()
        while new_count <= count:
            time.sleep(0.5)
            new_count = get_items_quantity()

        driver.back()
        count = new_count

    # open card
    driver.find_element_by_link_text("Checkout »").click()
    items_count = get_items_count_from_table()

    # clear basket
    while items_count > 0:
        remove_item_from_basket()
        items_count = get_items_count_from_table()
