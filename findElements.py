from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class ElementFinder():
    def __init__(self, driver):
        self.driver= driver
    def find_element_by_name(self,name, wait=10):
        count = 0
        while count < wait:
            try:
                elem = self.driver.find_element(By.NAME, name)
                print("found!")
                return elem

            except Exception as e:
                print("still searching")
                count += 1
                time.sleep(1)
    def find_element_by_xpath(self,xpath, wait=10):
        count = 0
        while count < wait:
            try:
                elem = self.driver.find_element(By.XPATH, xpath)
                print("found!")
                return elem

            except Exception as e:
                print("still searching")
                count += 1
                time.sleep(1)
