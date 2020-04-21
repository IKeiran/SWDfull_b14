from selenium.webdriver import Chrome

driver_path = '/Users/keiran/Downloads/chromedriver'
driver = Chrome(executable_path=driver_path)
driver.implicitly_wait(3)
base_url = 'https://opensource-demo.orangehrmlive.com/'
driver.get(base_url)
driver.close()
