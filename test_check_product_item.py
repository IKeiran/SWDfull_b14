import pytest
from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
import re

@pytest.fixture(scope="session")
def setup_environment():
    global driver
    driver = Firefox()
    driver.implicitly_wait(3)
    yield
    driver.close()


def test_check_product_item(setup_environment):
    base_url = 'http://192.168.64.2/litecart/'
    driver.get(base_url)
    xpath = "//div[@id='box-campaigns']//li[@class='product column shadow hover-light']"
    item = driver.find_elements_by_xpath(xpath)[0]
    name = item.find_element_by_class_name("name").text
    price_xpath = "//s[@class='regular-price']"
    price = item.find_element_by_xpath(price_xpath).text
    colors = item.find_element_by_xpath(price_xpath).value_of_css_property('color')
    r, g, b = re.search('\(.*\)', str(colors))[0][1:-1].split(',')[0:3]
    assert r.strip() == g.strip() == b.strip(), "Color is not gray"

    campaign_price_xpath = "//strong[@class='campaign-price']"
    campaign_price = item.find_element_by_xpath(campaign_price_xpath).text
    colors = item.find_element_by_xpath(campaign_price_xpath).value_of_css_property('color')
    r, g, b = re.search('\(.*\)', str(colors))[0][1:-1].split(',')[0:3]


    assert g.strip() == b.strip() == '0', "Color is not red"

    price_font_size = float(item.find_element_by_xpath(price_xpath).value_of_css_property('font-size')[:-2])
    campaign_price_font_size = float(
        item.find_element_by_xpath(campaign_price_xpath).value_of_css_property('font-size')[:-2])
    assert price_font_size < campaign_price_font_size, "Campaign price font size is smaller"

    driver.find_element_by_partial_link_text(name).click()
    product_name = driver.find_element_by_xpath('//h1[@class="title"]').text
    assert product_name == name

    product_price_xpath = "//s[@class='regular-price']"
    product_price = driver.find_element_by_xpath(product_price_xpath).text
    colors = driver.find_element_by_xpath(product_price_xpath).value_of_css_property('color')
    r, g, b = re.search('\(.*\)', str(colors))[0][1:-1].split(',')[0:3]
    assert r.strip() == g.strip() == b.strip(), "Color is not gray"
    assert product_price == price

    product_campaign_price_xpath = "//strong[@class='campaign-price']"
    product_campaign_price = driver.find_element_by_xpath(product_campaign_price_xpath).text
    colors = driver.find_element_by_xpath(product_campaign_price_xpath).value_of_css_property('color')
    r, g, b = re.search('\(.*\)', str(colors))[0][1:-1].split(',')[0:3]
    assert g.strip() == b.strip() == '0', "Color is not red"
    assert campaign_price == product_campaign_price

    price_font_size = float(driver.find_element_by_xpath(price_xpath).value_of_css_property('font-size')[:-2])
    campaign_price_font_size = float(
        driver.find_element_by_xpath(campaign_price_xpath).value_of_css_property('font-size')[:-2])
    assert price_font_size < campaign_price_font_size, "Campaign price font size is smaller"
