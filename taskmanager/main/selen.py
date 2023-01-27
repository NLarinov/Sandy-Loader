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
        self.count = ['download', 'load', 'скачать',
                      'загрузить', 'файл', 'pdf', 'txt', 'mp3', 'mp4']
        self.blocked = ['https://avidreaders.ru', ]
        self.used = []
        self.req = ''

    def antivirus(self, link, file):
        aa = self.antidriver.find_element(By.XPATH, '//*[@id="url_to_scan"]')
        aa.clear()
        aa.send_keys(link)
        try:
            self.antidriver.find_element(By.XPATH, '//*[@id="drwebscanformURL"]/div/div[2]/button').click()
        except ElementClickInterceptedException:
            try:
                self.antidriver.find_element(By.XPATH,
                                             '//*[@id="urolog"]/div/div[3]/table[2]/tbody/tr[1]/td[2]/a').click()
            except Exception:
                pass
        time.sleep(4)
        with open('result.txt', 'a') as line:
            try:
                c = self.antidriver.find_element(By.XPATH, '//*[@id="urolog"]/div/div[2'
                                                           ']/div/div/table/tbody/tr/td[1]/span').text
                if c == 'Вирусов нет':
                    line.write(f'Name: {file[13:]}, link: {link}, status: clear\n')
                else:
                    line.write(f'Name: {file[13:]}, link: {link}, status: dangerous\n')
                self.antidriver.find_element(By.XPATH, '//*[@id="urolog"]/div/div[3]'
                                                       '/table[2]/tbody/tr[1]/td[1]/a').click()
            except Exception:
                line.write(f'Name: {file[13:]}, link: {link}, status: undefined\n')

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

    def easy_download(self, login, req):
        print("Looking for a files...", end='\n\n')
        self.used = []
        self.req = req
        while True:
            self.driver.get(login)
            time.sleep(1)
            results = self.driver.find_elements(By.XPATH, '//a')
            [results.append(i) for i in self.driver.find_elements(By.XPATH, '//p')]
            [results.append(i) for i in self.driver.find_elements(By.XPATH, '//span')]
            [results.append(i) for i in self.driver.find_elements(By.XPATH, '//button')]
            print(len(results))
            if self.script(login, results) is True:
                print('SUCCESS')
                break

    def script(self, login, results, recursion=False):
        for i in results:
            name = self.get_attributes(i)
            if name in self.used:
                continue
            if any([True if j in str(name).lower() or j in i.text.lower() else False for j in self.count]) is True:
                print("Checking file...")
                try:
                    main = i.get_attribute('href')
                    i.click()
                    print('clicked')
                    self.used.append(name)
                    self.driver.switch_to.window(self.driver.window_handles[0])
                except ElementNotInteractableException:
                    print("Wrong element", end='\n\n')
                    self.used.append(name)
                    return False
                except ElementClickInterceptedException:
                    print('Error', end='\n\n')
                    self.used.append(name)
                    return False

                if self.driver.current_url != login:
                    if recursion is True:
                        return False
                    else:
                        new = self.driver.current_url
                        while True:
                            self.driver.get(new)
                            time.sleep(1)
                            results2 = self.driver.find_elements(By.XPATH, '//a')
                            [results2.append(i) for i in self.driver.find_elements(By.XPATH, '//p')]
                            print(len(results2))
                            if self.script(new, results2, recursion=True) is True:
                                print('SUCCESS')
                                with open('result.txt', 'w') as line:
                                    line.write('\n')
                                break
                        return False

                if len(os.listdir('C:\Downloads')) != 0:
                    print('File successfully downloaded!', end='\n\n')
                    files = glob.glob('C:\Downloads\*')
                    if main is None:
                        main = self.driver.current_url
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
        return True
