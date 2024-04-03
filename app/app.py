from selenium import webdriver
import time

print("Test Execution Started")
options = webdriver.ChromeOptions()
options.add_argument("--ignore-ssl-errors=yes")
options.add_argument("--ignore-certificate-errors")
driver = webdriver.Remote(
    command_executor="http://172.17.0.4:4444/wd/hub", options=options
)
# maximize the window size
driver.maximize_window()
time.sleep(5)
# navigate to browserstack.com
driver.get("https://longansorter-admin.web.app/login")
time.sleep(5)
# click on the Get started for free button
try:
    find_elem = driver.find_element("input", "Get started free")
    print(f"find elem - {find_elem}")
    find_elem.send_keys("abcdefg")
    time.sleep(10)
except Exception as e:
    pass
# close the browser
driver.close()
driver.quit()
print("Test Execution Successfully Completed!")
