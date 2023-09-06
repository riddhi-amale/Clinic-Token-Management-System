# from twilio.rest import Client

# from_whatsapp_number = 'whatsapp:+919637345585'
# to_whatsapp_number = 'whatsapp:+919833841218'
# client = Client()
# client.messages.create(body='First text',from_ = from_whatsapp_number, to= to_whatsapp_number)
# import pywhatkit 
# pywhatkit.sendwhatmsg("+919833841218","Hello",15,42)

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pyperclip
from config import CHROME_PROFILE_PATH 
from selenium.webdriver.chrome.options import Options

# Replace below path with the absolute path
# to chromedriver in your computer
options = webdriver.ChromeOptions()
options.add_argument(CHROME_PROFILE_PATH)
chrome_options= Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='F:\Shah_Clinic\chrome_driver\chromedriver.exe',options=options,chrome_options=chrome_options)
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 600)

# Replace 'Friend's Name' with the name of your friend
# or the name of a group
target = "Swapnil VJTI"

# Replace the below string with your own message
string = "HeyAaaaaa"

search_xpath = '//*[@id="side"]/div[1]/div/label/div/div[2]'
search_box = wait.until(EC.presence_of_element_located((
	By.XPATH, search_xpath)))
search_box.clear()
time.sleep(1)
pyperclip.copy(target)
search_box.send_keys(Keys.SHIFT,Keys.INSERT)
time.sleep(2)
target_xpath = f'//span[@title="{target}"]'
target_title = driver.find_element_by_xpath(target_xpath)
target_title.click()
time.sleep(1)
inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
input_box = driver.find_element_by_xpath(inp_xpath)
pyperclip.copy(string)
input_box.send_keys(Keys.SHIFT,Keys.INSERT)
input_box.send_keys(Keys.ENTER)
time.sleep(2)

