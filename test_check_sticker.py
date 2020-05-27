import time
import pytest
from selenium.webdriver import Chrome


@pytest.fixture(scope="session")
def setup_environment():
    global driver
    driver = Chrome()
    driver.implicitly_wait(3)
    yield
    time.sleep(5)
    driver.close()


def test_check_sticker(setup_environment):
    base_url = 'http://192.168.64.2/litecart/'
    driver.get(base_url)
    xpath = "//li[@class='product column shadow hover-light']"
    goods_items = driver.find_elements_by_xpath(xpath)
    for item in goods_items:
        sticker_count = item.find_elements_by_class_name('sticker')
        assert 1 == (len(sticker_count))
