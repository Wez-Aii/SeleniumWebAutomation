import asyncio
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

COMMAND_EXECUTOR = os.getenv("COMMAND_EXECUTOR", "http://172.17.0.3:4444/wd/hub")
WEBSITE_URL = os.getenv("WEBSITE", "www.google.com")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


class SeleniumRemoteWebAutomation:
    def __init__(self, web_driver_type, remote_url):
        self.driver = self.driver_setup(web_driver_type, remote_url)

    def driver_setup(self, web_driver_type, remote_url):
        _driver = None
        if web_driver_type == 'firebase':
            options = webdriver.FirefoxOptions()
        elif web_driver_type == 'chrome':
            options = webdriver.ChromeOptions()
        else:
            return _driver
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        _driver = webdriver.Remote(command_executor=remote_url, options=options)
        _driver.maximize_window()
        return _driver
    
    def close_driver(self):
        self.driver.close()

    def quit_driver(self):
        self.driver.quit()


class CustomWebAutomation(SeleniumRemoteWebAutomation):
    def __init__(self, web_driver_type, remote_url, website_url, username, password):
        super().__init__(web_driver_type, remote_url)
        self._website_url = website_url
        self._username = username
        self._password = password
        self._website_url = website_url

    async def login(self):
        try:
            self.driver.get(self._website_url)
            find_elem = self.driver.find_element(By.XPATH, "//input[@placeholder='กรุณากรอกชื่อผู้ใช้']")
            find_elem.send_keys(USERNAME)
            time.sleep(2)
            find_elem = self.driver.find_element(By.XPATH, "//input[@placeholder='กรุณากรอกรหัสผ่าน']")
            find_elem.send_keys(PASSWORD)
            time.sleep(2)

            self.driver.find_element(By.XPATH, "//button[@type='button']").click()
            time.sleep(2)
        except Exception as e:
            raise Exception(str(e)) 
        
    async def select_menu_btn(self, menu_btn_name: str='factory'):
        try:
            menu_btn = self.driver.find_element(By.XPATH, f"//div[@class='menus']//a[@href='/{menu_btn_name}']")
            menu_btn.click()
            time.sleep(1)
        except Exception as e:
            raise Exception(str(e)) 
        
    async def back_to_listpage(self):
        try:
            while True:
                _back_btns = self.driver.find_elements(By.XPATH, "//div[@class='back-btn']")
                if len(_back_btns) > 0:
                    _back_btns[-1].click()
                    await asyncio.sleep(3)
                else:
                    break
        except Exception as e:
            raise Exception(str(e))   

    async def click_create_factory_btn(self):
        try:
            _create_factory_btns = self.driver.find_elements(By.XPATH, "//img[@alt='i-factory']")
            if len(_create_factory_btns) > 0:
                _create_factory_btns[-1].find_element(By.XPATH, "..").click()
                await asyncio.sleep(3)
        except Exception as e:
            raise Exception(str(e))     
        
    async def map_to_factory_detail(self, factory_name: str = None):
        clickable_factories_icons = self.driver.find_elements(By.XPATH, "//div[@role='button']")
        for each in clickable_factories_icons:
            logging.debug(f"Searching Factory - {factory_name}")
            logging.debug(f"Current Icon Factory - {each.get_attribute('title')}")
            if each.get_attribute('title') == factory_name:
                logging.debug("Searching Factory Found")
                each.click()
                time.sleep(3)

    async def factory_detail_to_factory_configs_list(self):
        try:
            factory_configs_btn = self.driver.find_elements(By.XPATH, "//div[@class='item']//button[@class='action-btn']//img[@alt='i-options-gray']")
            if len(factory_configs_btn) > 0:
                factory_configs_btn[-1].find_element(By.XPATH, "..").click()
                await asyncio.sleep(3)
            else:
                factory_configs_btn = self.driver.find_elements(By.XPATH, "//div[@class='item']//button[@class='action-btn blue']//img[@alt='i-options']")
                if len(factory_configs_btn) > 0:
                    factory_configs_btn[-1].find_element(By.XPATH, "..").click()
                    await asyncio.sleep(3)
        except Exception as e:
            raise Exception(str(e))      

    def get_factories_list_elements(self):
        _factories = self.driver.find_elements(By.XPATH, "//div[@class='detail']//div[@class='name']")
        return _factories
    
    async def fill_factory_detail(self, factory_name:str, factory_abbr:str):
        try:
            # fill factory name
            self.driver.find_element(By.XPATH, "//input[@placeholder='กรุณากรอกชื่อโรงงาน']").send_keys(factory_name)
            await asyncio.sleep(1)

            # fill factory abbreviation 
            self.driver.find_element(By.XPATH, "//input[@placeholder='กรุณากรอกชื่อย่อโรงงาน']").send_keys(factory_abbr)
            await asyncio.sleep(1)

            # select customer group
            self.driver.find_element(By.XPATH, "//div[@class='left-wrap']//div[@class='form-group']//div[@popupclassname='select-dropdown']").click()
            await asyncio.sleep(1)
            customer_groups = self.driver.find_elements(By.XPATH, "//span[@class='ant-select-item-option-state']")
            if len(customer_groups) > 0:
                customer_groups[0].find_element(By.XPATH, "..").click()
                time.sleep(3)
            self.driver.find_element(By.XPATH, "//div[@class='right-wrap']//div[@class='form-group']//div[@popupclassname='select-dropdown']").click()
            await asyncio.sleep(1)
            available_machines = self.driver.find_elements(By.XPATH, "//div[@machine_status_info='New Machine']")
            if len(available_machines) > 0:
                available_machines[0].click()
                time.sleep(3)
        except Exception as e:
            raise Exception(str(e)) 
    
    async def factory_detail_test(self):
        await self.login()
        await self.select_menu_btn('factory')
        factories = self.get_factories_list_elements()
        for each in factories[1:4]:
            each.click()
            time.sleep(1)
            await self.map_to_factory_detail(each.get_attribute('title'))
            await self.factory_detail_to_factory_configs_list()
            await self.back_to_listpage()
            await self.select_menu_btn('factory')

    async def create_factory_automation(self):
        await self.login()
        await self.select_menu_btn('factory')
        await self.click_create_factory_btn()
        await self.fill_factory_detail(factory_name="factory1111111", factory_abbr="f1111")
        time.sleep(3)

    def test(self):
        try:
            factories = self.driver.find_elements(By.XPATH, "//div[@class='detail']//div[@class='name']")
            if len(factories) > 3:
                factories[0].click()
                time.sleep(2)
                factories[1].click()
                time.sleep(2)
                # factories[2].click()
                # time.sleep(2)
                f_icon_2_click = self.driver.find_elements(By.XPATH, "//div[@role='button']")
                for each in f_icon_2_click:
                    print("factory title - ", factories[1].get_attribute("title"))
                    print("each title -", each.get_attribute("title"))
                    if each.get_attribute("title") == factories[1].get_attribute("title"):
                        print("found")
                        each.click()
                        time.sleep(5)
        except Exception as e:
            raise Exception(str(e)) 
        
    async def test_run(self):
        await self.login()
        await self.select_menu_btn('factory')
        self.test()

if __name__=='__main__':
    selen_instance = CustomWebAutomation(web_driver_type='chrome', remote_url=COMMAND_EXECUTOR, website_url=WEBSITE_URL, username=USERNAME, password=PASSWORD)
    try:
        print("Test Execution Started")
        asyncio.run(selen_instance.create_factory_automation())
    except Exception as e:
        print(e)
        pass
    selen_instance.close_driver()
    selen_instance.quit_driver()