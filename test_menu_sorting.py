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


def test_countries_sorting(setup_environment):
    base_url = 'http://192.168.64.2/litecart/admin/'
    driver.get(base_url)
    login(driver)
    countries_link = 'http://192.168.64.2/litecart/admin/?app=countries&doc=countries&doc=countries'
    driver.get(countries_link)
    zone_list = list()
    zones = driver.find_elements_by_xpath("//tr[@class='row']")
    country_col = 4
    zone_count_column = 5
    non_zero_indexes = list()
    for index, row in enumerate(zones):
        zone = row.find_elements_by_css_selector("td")[country_col].text
        zone_list.append(str(zone))
        zone_count = row.find_elements_by_css_selector("td")[zone_count_column].text
        if zone_count != "0":
            non_zero_indexes.append(index)

    assert zone_list == sorted(zone_list)

    sub_zones_name_index = 2
    for index in non_zero_indexes:
        driver.get(countries_link)
        zone = driver.find_elements_by_xpath("//tr[@class='row']")[index]
        zone.find_element_by_css_selector("td>a").click()
        sub_zones_list = list()
        # check sub-zones
        sub_zones = driver.find_elements_by_xpath("//table[@class='dataTable']/*/tr")[1:-1]
        for sub_zone in sub_zones:
            sub_zones_list.append(sub_zone.find_elements_by_css_selector('td')[sub_zones_name_index].text)
        assert sub_zones_list == sorted(sub_zones_list)
        driver.back()


def test_geozones_sorting(setup_environment):
    base_url = 'http://192.168.64.2/litecart/admin/'
    driver.get(base_url)
    login(driver)
    geozones_link = 'http://192.168.64.2/litecart/admin/?app=geo_zones&doc=geo_zones'
    driver.get(geozones_link)
    zone_list = list()
    row_xpath = "//table[@class='dataTable']/*/tr[@class='row']"
    zones = driver.find_elements_by_xpath(row_xpath)
    sub_zones_name_col = 2
    print(len(zones))
    for index in range(len(zones)):
        driver.find_elements_by_xpath(row_xpath)[index].find_element_by_css_selector('td>a').click()
        time.sleep(2)
        sub_zones = driver.find_elements_by_xpath("//table[@class='dataTable']/*/tr")[1:-1]
        sub_zones_list = list()
        for sub_zone in sub_zones:
            sub_zones_list.append(sub_zone.find_elements_by_css_selector('td')[sub_zones_name_col].text)
        assert sub_zones_list == sorted(sub_zones_list)
        driver.back()


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
