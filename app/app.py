import asyncio
import logging
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import os

COMMAND_EXECUTOR = os.getenv("COMMAND_EXECUTOR", "http://172.17.0.3:4444/wd/hub")
WEBSITE_URL = os.getenv("WEBSITE", "www.google.com")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

X_Y_COORDINATE_POINTS = [
                (-220,-200),(-140,-200),(-60,-200),(20,-200),(100,-200),(180,-200),
                (-240,-120),(-160,-120),(-80,-120),(0,-120),(80,-120),(160,-120),(240,-120),
                (-220,-40),(-140,-40),(-60,-40),(20,-40),(100,-40),(180,-40),
                (-240,40),(-160,40),(-80,40),(0,40),(80,40),(160,40),(240,40),
                (-220,120),(-140,120),(-60,120),(20,120),(100,120),(180,120),
                (-240,200),(-160,200),(-80,200),(0,-200),(80,200),(160,200),(240,200)
                                     ]

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
    
    def random_click_in_element(self, target_element, exclusion_horizontal_padding_px=60, exclusion_verticle_padding_px=100):
        # Get dimensions of the div
        print(target_element.rect)
        div_location = target_element.location
        div_size = target_element.size
        div_x = div_location['x']
        div_y = div_location['y']
        div_width = div_size['width']
        div_height = div_size['height']

        div_max_x = int(div_width/2)
        div_max_y = int(div_height/2)

        valid_max_x = div_max_x - exclusion_horizontal_padding_px
        valid_max_y = div_max_y - exclusion_verticle_padding_px

        random_x = random.randint(-valid_max_x, valid_max_x)
        random_y = random.randint(-valid_max_y, valid_max_y)
        print(f"random_x , random_y - ({random_x}, {random_y})")

        # Perform mouse click at the random coordinates
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(target_element, -240, -200)
        # actions.move_to_element_with_offset(target_element, 0, 0)
        # actions.move_to_element_with_offset(target_element, random_x, random_y)
        # actions.move_by_offset(random_x - div_x, random_y - div_y)
        actions.click()
        actions.perform()
    
    def coordinates_target_click_in_element(self, target_element, x_coordinate:int=0, y_coordinate:int=0):
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(target_element, x_coordinate, y_coordinate)
        actions.click()
        actions.perform()
    
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
        self._x_y_coordinate_points = X_Y_COORDINATE_POINTS

    async def login(self):
        try:
            self.driver.get(self._website_url)
            find_elem = self.driver.find_element(By.XPATH, "//input[@placeholder='กรุณากรอกชื่อผู้ใช้']")
            find_elem.send_keys(USERNAME)
            time.sleep(0.2)
            find_elem = self.driver.find_element(By.XPATH, "//input[@placeholder='กรุณากรอกรหัสผ่าน']")
            find_elem.send_keys(PASSWORD)
            time.sleep(1)

            self.driver.find_element(By.XPATH, "//button[@type='button']").click()
            time.sleep(3)
        except Exception as e:
            raise Exception(str(e)) 
        
    async def select_menu_btn(self, menu_btn_name: str='factory'):
        try:
            menu_btn = self.driver.find_element(By.XPATH, f"//div[@class='menus']//a[@href='/{menu_btn_name}']")
            menu_btn.click()
            time.sleep(3)
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
            
    async def back_to_prevpage(self):
        try:
            _back_btns = self.driver.find_elements(By.XPATH, "//div[@class='back-btn']")
            if len(_back_btns) > 0:
                _back_btns[-1].click()
                await asyncio.sleep(3)
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
    
    async def fill_factory_detail(self, factory_name:str, factory_abbr:str, index:int=0):
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
                time.sleep(1)            

            # select map coordinate
            _map_icons =self.driver.find_elements(By.XPATH, "//img[@alt='i-map']")
            if len(_map_icons) > 0:
                _map_icons[-1].find_element(By.XPATH, "..").click()
                time.sleep(1)
            # _map_divs = self.driver.find_elements(By.XPATH, "//div[@aria-label='Map']")
            _map_divs = self.driver.find_elements(By.XPATH, "//div[@class='mapdiv']")
            if len(_map_divs) > 0:
                # _x_coordinate = self._x_y_coordinate_points[index][0]
                # _y_coordinate = self._x_y_coordinate_points[index][1]
                _x_coordinate = 0
                _y_coordinate = 0
                self.coordinates_target_click_in_element(target_element=_map_icons[-1].find_element(By.XPATH, "//iframe[@aria-hidden='true']"), x_coordinate=_x_coordinate, y_coordinate=_y_coordinate)
                time.sleep(2)
            _btns = self.driver.find_elements(By.XPATH, "//div[@class='header']//div[@class='action-wrap']//div[@class='item']//button[@type='button']")
            if len(_btns) > 0:
                _btns[-1].click()
                time.sleep(2)

            # for i in range(39):
            #     # _map_divs = self.driver.find_elements(By.XPATH, "//div[@aria-label='Map']")
            #     _map_divs = self.driver.find_elements(By.XPATH, "//div[@class='mapdiv']")
            #     if len(_map_divs) > 0:
            #         _x_coordinate = self._x_y_coordinate_points[i][0]
            #         _y_coordinate = self._x_y_coordinate_points[i][1]
            #         self.coordinates_target_click_in_element(target_element=_map_icons[-1].find_element(By.XPATH, "//iframe[@aria-hidden='true']"), x_coordinate=_x_coordinate, y_coordinate=_y_coordinate)
            #         time.sleep(2)
            #     # await self.back_to_prevpage()
            #     time.sleep(3)
            
            # fill factory address 
            self.driver.find_element(By.XPATH, "//textarea[@placeholder='ที่อยู่โรงงาน']").send_keys(f"Post Address of {factory_name}")
            await asyncio.sleep(1)

            # fill factory contact infos
            # fill firstnames for contact 1 and 2
            firstnames_inputfields = self.driver.find_elements(By.XPATH, "//input[@placeholder='ชื่อ']")
            _temp_index = 1
            for each in firstnames_inputfields:
                each.send_keys(f"fun_fn_{_temp_index}")
                _temp_index += 1
                await asyncio.sleep(1)

            # fill lastnames for contact 1 and 2
            lastnames_inputfields = self.driver.find_elements(By.XPATH, "//input[@placeholder='นามสกุล']")
            _temp_index = 1
            for each in lastnames_inputfields:
                each.send_keys(f"fun_ln_{_temp_index}")
                _temp_index += 1
                await asyncio.sleep(1)

            # fill phone number for contact 1 and 2
            lastnames_inputfields = self.driver.find_elements(By.XPATH, "//input[@placeholder='เบอร์โทรติดต่อ']")
            _temp_index = 1
            for each in lastnames_inputfields:
                each.send_keys(f"09{random.randint(1,99999999)}")
                _temp_index += 1
                await asyncio.sleep(1)

            # allocate new machine to factory
            self.driver.find_element(By.XPATH, "//div[@class='right-wrap']//div[@class='form-group']//div[@popupclassname='select-dropdown']").click()
            await asyncio.sleep(3)
            available_machines = self.driver.find_elements(By.XPATH, "//div[@machine_status_info='New Machine']")
            if len(available_machines) > 0:
                available_machines[0].click()
                time.sleep(1)

            # click submit btn to save
            _btns = self.driver.find_elements(By.XPATH, "//div[@class='header']//div[@class='action-wrap']//div[@class='item']//button[@type='button']")
            if len(_btns) > 0:
                _btns[-1].click()
                time.sleep(2)
                
            # click confirm btn to save submit
            _btns = self.driver.find_elements(By.XPATH, "//div[@class='action-btn-wrap']//div[@class='action-btn']//button[@type='button']")
            if len(_btns) > 0:
                _btns[-1].click()
                time.sleep(2)
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

    async def create_factory_automation(self, n_factory:int=1, factory_count_start:int=0):
        await self.login()
        await self.select_menu_btn('factory')
        await self.click_create_factory_btn()
        for i in range(factory_count_start, factory_count_start + n_factory):
            await self.fill_factory_detail(factory_name="factory1111111", factory_abbr="f1111", index=i)
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