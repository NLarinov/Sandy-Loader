import time
from selenium import webdriver
from selenium.common import ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
import keyboard
from multiprocessing import Process
from selenium.webdriver.firefox.options import Options
import os
import glob


class TestClass:
    def __init__(self):
        profile = Options()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.dir", 'C:\Downloads')
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
        self.antidriver = webdriver.Firefox()
        self.antidriver.get('https://vms.drweb.ru/online/')
        self.driver = webdriver.Firefox(options=profile)
        self.count = ['download', 'load', 'mb', 'kb', 'gb', 'скачать',
                      'загрузить', 'установить', 'get', 'link', 'файл']

    def antivirus(self, link, file):
        try:
            self.antidriver.find_element(By.XPATH,
                                         '//*[@id="urolog"]/div/div[3]/table[2]/tbody/tr[1]/td[2]/a').click()
        except Exception:
            pass
        aa = self.antidriver.find_element(By.XPATH, '//*[@id="url_to_scan"]')
        aa.clear()
        aa.send_keys(link)
        self.antidriver.find_element(By.XPATH, '//*[@id="drwebscanformURL"]/div/div[2]/button').click()
        time.sleep(4)
        try:
            c = self.antidriver.find_element(By.XPATH, '//*[@id="urolog"]/div/div[2'
                                                       ']/div/div/table/tbody/tr/td[1]/span').text
            print(c)
            if c == 'Вирусов нет':
                print(file, link, 'clear')
            else:
                print(file, link, 'dangerous')
            self.antidriver.find_element(By.XPATH, '//*[@id="urolog"]/div/div[3]/table[2]/tbody/tr[1]/td[1]/a').click()
        except Exception:
            print(file, link, 'undefined')

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

        error_list = []

        results = self.driver.find_elements(By.XPATH, '//a')
        print(len(results))

        for i in results:
            name = self.get_attributes(i)
            if name in error_list:
                continue
            print("Checking file...")
            flag = False
            for j in self.count:
                if j in str(name).lower():
                    flag = True
                    break
            if flag is True:
                try:
                    main = i.get_attribute('href')
                    i.click()
                    print('clicked')
                    self.driver.switch_to.window(self.driver.window_handles[0])
                except ElementNotInteractableException:
                    print("Wrong element", end='\n\n')
                    error_list.append(name)
                    continue
                except ElementClickInterceptedException:
                    print('Error')
                    error_list.append(name)
                    continue

                if len(os.listdir('C:\Downloads')) != 0:
                    print('File successfully downloaded!', end='\n\n')
                    error_list.append(name)
                    files = glob.glob('C:\Downloads\*')
                    self.antivirus(main, files[0])

                    if len(files) == 2:
                        keyboard.send('tab')
                        for k in range(100):
                            keyboard.send('up arrow')
                        keyboard.send('tab')
                        keyboard.send('enter')
                        time.sleep(0.5)
                    else:
                        for f in files:
                            os.remove(f)
                else:
                    print('File was not detected', end='\n\n')
                    error_list.append(name)
