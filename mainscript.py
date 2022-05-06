#Author Filip Malmberg

import time
import os
import sys
import subprocess


from splinter import Browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def ping(host):
    try:
        output = subprocess.check_output("ping -{} 3 {}".format('n' if platform.system().lower()=="windows" else 'c', host), shell=True)
    except Exception:
        return False
    return True

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

while True:
    print('Pinging unit')
    if ping('192.168.1.253') == True:
        break
    else:
        print('Unit not responsive, trying again.')
        print('Are your IP address settings correct?')
        print('Try setting your IP address to 192.168.1.200 and subnet to 255.255.255.0')

driver = webdriver.Firefox()
driver.get('http://192.168.1.253')
driver.implicitly_wait(5)
firmware = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div[4]/div/fieldset[1]/fieldset/div[1]/div"))).text
serial = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div[4]/div/fieldset[2]/fieldset/div[5]/div"))).text
hardwareversion = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div[4]/div/fieldset[2]/fieldset/div[2]/div"))).text

if "AY" in hardwareversion:
    print('Device already has the correct hardwareversion')

elif "AY" not in hardwareversion:
    print("Wrong hardwareversion detected. Hardwareversion is {}. Attempting to apply hotfix".format(hardwareversion))
    toolsbutton = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div[1]/ul/li[2]/a")
    toolsbutton.click() #Click on tools
    driver.implicitly_wait(5)
    loginbutton = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div[4]/form/div[2]/input[1]")
    loginbutton.click() #Click on login
    driver.implicitly_wait(5)
    configbutton = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div[3]/table/tbody/tr/td/table/tbody/tr[5]/td/a")
    configbutton.click() #Click on firmware upgrade
    driver.implicitly_wait(5)
    browsebutton = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div[4]/div[1]/fieldset/fieldset/form/div[1]/div/input[@type='file']").send_keys(os.getcwd()+"\\RAILBOX66AY-PATCH.BIN")
    driver.implicitly_wait(5)
    restorebutton = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div[4]/div[1]/fieldset/fieldset/form/div[2]/div/input")
    restorebutton.click()
    driver.implicitly_wait(5)
    countdown(int(60))
    while True:
        print('Pinging unit')
        if ping('192.168.1.253') == True:
            break
        else:
            print('Unit not responsive, trying again.')
    driver.get('http://192.168.1.253')
    driver.implicitly_wait(20)
    hardwareversion = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div[4]/div/fieldset[2]/fieldset/div[2]/div"))).text
    if "AY" in hardwareversion:
        print(hardwareversion)
        print('Success!')
    else:
        print('Update failed...')

else:
    print('Unknown error occured')