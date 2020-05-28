from Locators.locators import Locators
class AdminLoginPage:

    def __init__(self, driver):
        self.driver = driver

    def set_login(self, user_login):
        txt_username_name = Locators.admin_txt_username_name
        self.driver.find_element_by_name(txt_username_name).clear()
        self.driver.find_element_by_name(txt_username_name).send_keys(user_login)

    def set_password(self, user_password):
        txt_userpassword_name = Locators.admin_txt_userpassword_name
        self.driver.find_element_by_name(txt_userpassword_name).clear()
        self.driver.find_element_by_name(txt_userpassword_name).send_keys(user_password)

    def login_btn_click(self):
        btn_login_name = Locators.admin_btn_login_name
        self.driver.find_element_by_name(btn_login_name).click()

    def logout_btn_click(self):
        btn_logout_css = Locators.admin_btn_logout_css
        self.driver.find_element_by_css_selector(btn_logout_css).click()
