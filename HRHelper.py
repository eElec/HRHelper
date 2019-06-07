#!/usr/bin/env python
# > Create Folders and put problem statement, stdin and starting piece thingy 

import sys
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from PIL import Image

# Check
if (len(sys.argv) < 2):
	print('Usage: <<>>.py [url] \nSample url: https://www.hackerrank.com/challenges/attribute-parser/problem')
	exit()

# Run Firefox
firefoxOption = Options()
firefoxOption.add_argument('-headless');
firefoxOption.add_argument('--window-size=1920,1080')
driver = webdriver.Firefox(firefox_options=firefoxOption)
P_PATH = './'
URL = ''

# create nested folders
def createFolders():
	global P_PATH
	pathList = driver.find_elements_by_class_name('breadcrumb-item-text')
	for p in pathList:
		P_PATH += p.text + '/'
	os.makedirs(P_PATH, exist_ok=True)
	populateFolder()

# Put in the myeet
def populateFolder():
	ProblemStatement()
	ProblemCode()
	InputOutput()
	#Runner()

# [populateFolder]
# Creates an Image of the problem statement
# TODO: Add options whether to use text or image
def ProblemStatement():
	p_Statement = driver.find_element_by_class_name('hr_tour-problem-statement').screenshot_as_png
	img = open("{0}/statement.png".format(P_PATH), "wb")
	img.write(p_Statement)
	img.close()

# Makes the code file
def ProblemCode():
	global URL
	p_Lang = {"C++":"cpp", "Python":"py", "C":"c"}		#TODO: Add other langs
	p_Lang_Comment = {"C++":"//", "Python":"#", "C":"//"}

	pathList = driver.find_elements_by_class_name('breadcrumb-item-text')
	p_Name = ''.join(ch for ch in pathList[-1].text if ch.isalnum())
	p_default = driver.find_element_by_xpath("//div[@class='view-lines']").text		#TODO: prettify p_default
	
	pMain = open("{0}{1}.{2}".format(P_PATH, p_Name, p_Lang[pathList[1].text]), 'w')
	
	initComment = "{0} URL - {1}\n\n".format(p_Lang_Comment[pathList[1].text], URL)
	pMain.write(initComment)
	pMain.write(p_default)
	pMain.close()

def InputOutput():
	p_Input = driver.find_element_by_class_name('challenge_sample_input_body').text
	inp = open('{0}/inp.txt'.format(P_PATH), 'w')
	inp.write(p_Input)
	inp.close()

	p_Output = driver.find_element_by_class_name('challenge_sample_output_body').text
	out = open('{0}/out.txt'.format(P_PATH), 'w')
	out.write(p_Output)
	out.close()
	

def main():
	global URL 
	URL = sys.argv[1]
	driver.get(URL)
	# Close the signup popup 
	try:
		close_btn = driver.find_element_by_class_name('close-icon')
		close_btn.click()
	except:
		pass

	createFolders()

	driver.close()

if __name__ == "__main__":
	main()
