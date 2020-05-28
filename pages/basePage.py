class BasePage:

    def __init__(self, driver):
        self.base_url = 'https://litecart.stqa.ru/en/'
        self.driver = driver

    def open(self):
        self.driver.get(self.base_url)

    def get_items_quantity(self):
        items_quantity_xpath = "//span[@class='quantity']"
        return int(self.driver.find_element_by_xpath(items_quantity_xpath).text)

    def navigate_to_basket_page(self):
        self.driver.find_element_by_link_text("Checkout »").click()
