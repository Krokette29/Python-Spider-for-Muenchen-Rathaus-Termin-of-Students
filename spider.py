import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import os
import sys
import io


url = "https://www.muenchen.de/rathaus/terminvereinbarung_abh.html?cts=1089339"

def check():
	tds = driver.find_elements(By.TAG_NAME, 'td')
	for item in tds:
		if item.text and 'bookable' in item.get_attribute('class'):
			print('Find a termin at {}!'.format(time.asctime(time.localtime(time.time()))))
			print(item.text, item.get_attribute('class'))
			item.click()
			return True

	return False


driver = webdriver.Chrome()
driver.get(url)

driver.switch_to.frame('appointment')

Select(driver.find_element(By.TAG_NAME, 'select')).select_by_value('1')

button = driver.find_element(By.XPATH, '//*[@id="F00e214c9f52bf4cddab8ebc9bbb11b2b"]/fieldset/input[2]')
button.click()

while 'appoints' not in driver.page_source:
    time.sleep(1)

right = True
count = 0
while True:
	
    time.sleep(1)
    if check(): break
    
    buttons = driver.find_elements(By.CLASS_NAME, 'navButton')
    if right:
        for button in buttons:
            if button.text == '>':
                button.click()
                break
        count += 1
        if count == 3:
            right = False
            count = 0
    else:
        for button in buttons:
            if button.text == '<':
                button.click()
                break
        count += 1
        if count == 3:
            right = True
            count = 0

	# dates = re.findall('\d{4}-\d{2}-\d{2}', txt)
	# for date in dates:
	# 	res = re.search(date+'.{2}(.{2})', txt).group(1)
	# 	if res[1] != ']':
	# 		print('Find a termin in {date} at {time}'.format(date=date, time=time.asctime(time.localtime(time.time()))))



with open( '.\\output\\ouput_page_source.txt', 'w', encoding="utf-8") as f:
	f.write(driver.page_source)
