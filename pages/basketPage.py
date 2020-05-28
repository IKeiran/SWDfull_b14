class BasketPage:

    def __init__(self, driver):
        self.driver = driver

    def get_items_count_in_basket(self):
        table_xpath = "//table[@class='dataTable rounded-corners']/*/tr/td[@class='item']/.."
        items = self.driver.find_elements_by_xpath(table_xpath)
        items_count = 0
        for item in items:
            data = item.find_elements_by_xpath('.//td')[0]
            items_count += int(data.text)
        return items_count

    def remove_item_from_basket(self):
        remove_xpath = "//button[@name='remove_cart_item']"
        self.driver.find_element_by_xpath(remove_xpath).click()
        self.driver.refresh()

    def clear_basket(self):
        items_count = self.get_items_count_in_basket()
        # clear basket
        while items_count > 0:
            self.remove_item_from_basket()
            items_count = self.get_items_count_in_basket()
