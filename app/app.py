from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

COMMAND_EXECUTOR = os.getenv("COMMAND_EXECUTOR", "http://172.17.0.3:4444/wd/hub")
WEBSITE_URL = os.getenv("WEBSITE", "www.google.com")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

print("Test Execution Started")
# options = webdriver.ChromeOptions()
# options.add_argument("--ignore-ssl-errors=yes")
# options.add_argument("--ignore-certificate-errors")
# driver = webdriver.Remote(
#     command_executor=COMMAND_EXECUTOR, options=options
# )

options = webdriver.FirefoxOptions()
options.add_argument("--ignore-ssl-errors=yes")
options.add_argument("--ignore-certificate-errors")
driver = webdriver.Remote(command_executor=COMMAND_EXECUTOR, options=options)
# maximize the window size
driver.maximize_window()
time.sleep(2)
# navigate to browserstack.com
driver.get(os.getenv("WEBSITE"))
time.sleep(2)
# click on the Get started for free button
try:
    # find_elem = driver.find_element(By.ID, "APjFqb")
    find_elem = driver.find_element(By.XPATH, "//input[@placeholder='กรุณากรอกชื่อผู้ใช้']")
    find_elem.send_keys(USERNAME)
    time.sleep(2)
    find_elem = driver.find_element(By.XPATH, "//input[@placeholder='กรุณากรอกรหัสผ่าน']")
    find_elem.send_keys(PASSWORD)
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[@type='button']").click()
    time.sleep(5)
    factories = driver.find_elements(By.XPATH, "//div[@class='detail']//div[@class='name']")
    if len(factories) > 3:
        factories[0].click()
        time.sleep(2)
        factories[1].click()
        time.sleep(2)
        # factories[2].click()
        # time.sleep(2)
        f_icon_2_click = driver.find_elements(By.XPATH, "//div[@role='button']")
        for each in f_icon_2_click:
            print("factory title - ", factories[1].get_attribute("title"))
            print("each title -", each.get_attribute("title"))
            if each.get_attribute("title") == factories[1].get_attribute("title"):
                print("found")
                each.click()
                time.sleep(5)

except Exception as e:
    print(f"error occur - {e}")
    pass
# close the browser
driver.close()
# driver.quit()
print("Test Execution Successfully Completed!")


# class SeleniumRemoteWebAutomation:
#     def __init__(self, web_driver_type, remote_url):
#         self.driver = self.driver_setup(web_driver_type, remote_url)

#     def driver_setup(self, web_driver_type, remote_url):
#         _driver = None
#         if web_driver_type == 'firebase':
#             options = webdriver.FirefoxOptions()
#         elif web_driver_type == 'chrome':
#             options = webdriver.ChromeOptions()
#         else:
#             return _driver
#         options.add_argument("--ignore-ssl-errors=yes")
#         options.add_argument("--ignore-certificate-errors")
#         _driver = webdriver.Remote(command_executor=remote_url, options=options)
#         driver.maximize_window()
#         return _driver
    
#     def close_driver(self):
#         self.driver.close()

#     def quit_driver(self):
#         self.driver.quit()


# class CustomWebAutomation(SeleniumRemoteWebAutomation):
#     def __init__(self, web_driver_type, remote_url, website_url, username, password):
#         super().__init__(web_driver_type, remote_url)
#         self._website_url = website_url
#         self._username = username
#         self._password = password

#     def login(self):
#         try:
#             # find_elem = driver.find_element(By.ID, "APjFqb")
#             find_elem = self.driver.find_element(By.XPATH, "//input[@placeholder='กรุณากรอกชื่อผู้ใช้']")
#             find_elem.send_keys(USERNAME)
#             time.sleep(2)
#             find_elem = self.driver.find_element(By.XPATH, "//input[@placeholder='กรุณากรอกรหัสผ่าน']")
#             find_elem.send_keys(PASSWORD)
#             time.sleep(2)

#             self.driver.find_element(By.XPATH, "//button[@type='button']").click()
#         except Exception as e:
#             raise Exception(str(e)) 

#     def test(self):
#         try:
#             factories = driver.find_elements(By.XPATH, "//div[@class='detail']//div[@class='name']")
#             if len(factories) > 3:
#                 factories[0].click()
#                 time.sleep(2)
#                 factories[1].click()
#                 time.sleep(2)
#                 # factories[2].click()
#                 # time.sleep(2)
#                 f_icon_2_click = driver.find_elements(By.XPATH, "//div[@role='button']")
#                 for each in f_icon_2_click:
#                     print("factory title - ", factories[1].get_attribute("title"))
#                     print("each title -", each.get_attribute("title"))
#                     if each.get_attribute("title") == factories[1].get_attribute("title"):
#                         print("found")
#                         each.click()
#                         time.sleep(5)
#         except Exception as e:
#             raise Exception(str(e)) 

# if __name__=='__main__':
#     selen_instance = CustomWebAutomation(web_driver_type='chrome', remote_url=COMMAND_EXECUTOR, website_url=WEBSITE_URL, username=USERNAME, password=PASSWORD)
#     try:
#         selen_instance.login()
#     except Exception as e:
#         selen_instance.close_driver()