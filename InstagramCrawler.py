from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from getpass import getpass
import os
import requests as r

op = webdriver.ChromeOptions()
op.add_argument('headless')
op.add_argument('log-level=2')

browser = webdriver.Chrome(executable_path="chromedriver_win32\\chromedriver.exe", options=op)
browser.implicitly_wait(5)

browser.get("https://www.instagram.com/accounts/login/")

input_username = browser.find_element_by_css_selector("input[name='username']")
input_password = browser.find_element_by_css_selector("input[name='password']")

username = input("Please enter username: ")
password = getpass(prompt='Please enter password: ')

id = input("Please enter the id of the user you want to crawl (https://www.instagram.com/abc123 -> id is: abc123): ")
current_path = os.getcwd()
try: os.mkdir(current_path + "\\"+id+"\\")
except:pass

input_username.send_keys(username)
input_password.send_keys(password)

button_login = browser.find_element_by_xpath("//button[@type='submit']")
button_login.click()

sleep(3)

url = "https://www.instagram.com/"

browser.get(url+id)

last_height = browser.execute_script("return document.body.scrollHeight")

url_array = []
while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    data = browser.page_source
    soup = BeautifulSoup(data, 'html.parser')
    for a in soup.find_all('a', href=True):
        if a['href'].find("/p/") != -1:
            if a['href'] not in url_array:
                url_array.append(a['href'])
    sleep(2)

    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

for i in range(len(url_array)):
    browser.get(url+url_array[i])
    data = browser.page_source
    soup = BeautifulSoup(data, 'html.parser')
    for img in soup.find_all('img', {'class': 'FFVAD'}):
        print(url_array[i])
        if(img['src']):
            file_name = str(img['src']).split('/')[-1].split('?')[0]
            with open(id+'/'+ file_name, 'wb') as f:
                f.write(r.get(img['src']).content)
                f.close()
browser.close()