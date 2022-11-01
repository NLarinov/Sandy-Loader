import time
from selenium import webdriver
from selenium.common import ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import os
import glob


class TestClass:
    def __init__(self):
        profile = Options()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", 'C:\Downloads')
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
        self.driver = webdriver.Firefox(options=profile)

    def get_attributes(self, element) -> dict:
        return self.driver.execute_script(
            """
            let attr = arguments[0].attributes;
            let items = {}; 
            for (let i = 0; i < attr.length; i++) {
                items[attr[i].name] = attr[i].value;
            }
            return items;
            """,
            element
        )

    def easy_download(self, login):
        print("Starting and Logining...", end='\n\n')
        self.driver.get(login)
        time.sleep(1)
        print("Looking for a files...", end='\n\n')

        error = False
        error_list = []

        while True:
            results = self.driver.find_elements(By.XPATH, '//a')
            print(len(results))

            for i in results:
                name = self.get_attributes(i)
                print(i)
                if name in error_list:
                    continue
                print("Checking file...")
                if 'download' in str(name).lower() or 'load' in str(name).lower():
                    try:
                        i.get_attribute('href')
                        i.click()
                    except ElementNotInteractableException:
                        print("Wrong element", end='\n\n')
                        error_list.append(name)
                        continue
                    except ElementClickInterceptedException:
                        self.driver.get(login)
                        time.sleep(1)
                        error_list.append(name)
                        error = True
                        break

                    if self.driver.current_url != login:
                        self.driver.get(login)
                        time.sleep(1)
                        error_list.append(name)
                        error = True
                        break

                    if len(os.listdir('C:\Downloads')) != 0:
                        print('File successfully downloaded!', end='\n\n')
                        error_list.append(name)
                        files = glob.glob('C:\Downloads\*')
                        for f in files:
                            print(f)
                    else:
                        print('File was not detected', end='\n\n')
                        error_list.append(name)
                error = False
            if error is False:
                break

    def full_download(self, login):
        print("Starting and Logining...", end='\n\n')
        self.driver.get(login)
        time.sleep(1)
        print("Looking for a files...", end='\n\n')

        error = False
        error_list = []

        while True:
            results = self.driver.find_elements(By.XPATH, '//a')
            print(len(results))

            for i in results:
                name = self.get_attributes(i)
                print(i)
                if name in error_list:
                    continue
                print("Checking file...")
                try:
                    i.get_attribute('href')
                    i.click()
                except ElementNotInteractableException:
                    print("Wrong element", end='\n\n')
                    error_list.append(name)
                    continue
                except ElementClickInterceptedException:
                    self.driver.get(login)
                    time.sleep(1)
                    error_list.append(name)
                    error = True
                    break

                if self.driver.current_url != login:
                    self.driver.get(login)
                    time.sleep(1)
                    error_list.append(name)
                    error = True
                    break

                if len(os.listdir('C:\Downloads')) != 0:
                    print('File successfully downloaded!', end='\n\n')
                    error_list.append(name)
                    files = glob.glob('C:\Downloads\*')
                    for f in files:
                        print(f)
                else:
                    print('File was not detected', end='\n\n')
                    error_list.append(name)
                error = False
            if error is False:
                break