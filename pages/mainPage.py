from .basePage import BasePage

class MainPage(BasePage):

    def open_product_by_index(self, product_index):
        product_xpath = "//li[@class='product column shadow hover-light']"
        self.driver.find_elements_by_xpath(product_xpath)[product_index].click()