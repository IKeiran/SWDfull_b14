from .basePage import BasePage
import time


class ProductPage(BasePage):
    def add_product_to_basket(self):
        add_button_xpath = "//button[@name='add_cart_product']"
        count = self.get_items_quantity()
        self.driver.find_element_by_xpath(add_button_xpath).click()
        new_count = self.get_items_quantity()
        while new_count <= count:
            time.sleep(0.5)
            new_count = self.get_items_quantity()
