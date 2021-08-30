from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui as pag
import time


class EasyApplyer:

    def __init__(self):
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver = webdriver.Chrome(data['driver_path'])
