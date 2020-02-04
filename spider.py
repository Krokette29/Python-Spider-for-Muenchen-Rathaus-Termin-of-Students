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


# not sure whether it works or not
def check_termin():
	tds = driver.find_elements(By.TAG_NAME, 'td')
	for item in tds:
		if item.text:
			if 'bookable' in item.get_attribute('class'):
				print('Find a termin at {}!'.format(time.asctime(time.localtime(time.time()))))
				print(item.text, item.get_attribute('class'))
				item.click()
				return True
			item.click()
			
	time.sleep(1)

	if 'Eingabe der Kontaktdaten' in driver.page_source:
		print('Find a termin at {}!'.format(time.asctime(time.localtime(time.time()))))        
		return True

	return False


# export page source and cookies to the folder .\output
def export(record_num):
	with open( '.\\output\\page_source_{}.html'.format(record_num), 'w', encoding="utf-8") as f:
		f.write(driver.page_source)

	with open( '.\\output\\get_cookies_{}.txt'.format(record_num), 'w', encoding="utf-8") as f:
		f.write(str(driver.get_cookies()))


# to be finished
def termin_click():
	pass


def main():
	url = "https://www.muenchen.de/rathaus/terminvereinbarung_abh.html?cts=1089339"
	tic = time.asctime(time.localtime(time.time()))

	driver = webdriver.Chrome()
	driver.get(url)

	record_num = 0
	# main loop
	while True:      
		# wait for loading complete and switch to frame appointment
		succ = False
		while not succ:
			try:
				driver.switch_to.frame('appointment')
				succ = True
			except:
				time.sleep(1)

		# switch to next step: Standort
		Select(driver.find_element(By.TAG_NAME, 'select')).select_by_value('1')

		button = driver.find_element(By.XPATH, '//*[@id="F00e214c9f52bf4cddab8ebc9bbb11b2b"]/fieldset/input[2]')
		button.click()

		# wait for data from KVR
		while 'appoints' not in driver.page_source:
			time.sleep(1)

		refresh = False
		termin_exist = False
		
		# checking loop
		while True:            
			toc = time.asctime(time.localtime(time.time()))
			if check_termin(): 
				termin_exist = True
				break

			buttons = driver.find_elements(By.CLASS_NAME, 'navButton')
			for button in buttons:
				refresh = True
				if button.text == '>':
					button.click()
					print('click button right')
					refresh = False
					
					# export html source and cookies
					export(record_num)
					record_num += 1
					break
					
		if termin_exist: break
		if refresh: driver.refresh()

	export('succ')
	termin_click()


if __name__ == '__main__':
	main()
