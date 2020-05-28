import time
import pytest
from selenium.webdriver import Chrome
from pages.basketPage import BasketPage
from pages.mainPage import MainPage
from pages.productPage import ProductPage


@pytest.fixture(scope="session")
def setup_environment():
    global driver
    driver = Chrome()
    driver.implicitly_wait(3)
    yield
    time.sleep(5)
    driver.close()


def test_shopping_card(setup_environment):
    main_page = MainPage(driver=driver)
    product_page = ProductPage(driver=driver)
    basket_page = BasketPage(driver=driver)
    main_page.open()
    # fill shopping card by products
    max_items = 3
    for _ in range(max_items):
        main_page.open_product_by_index(0)
        product_page.add_product_to_basket()
        main_page.open()

    # open card
    main_page.navigate_to_basket_page()
    basket_page.clear_basket()
    assert 0 == basket_page.get_items_count_in_basket()
