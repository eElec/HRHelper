#!/usr/bin/env python
# > Create Folders and put problem statement, stdin and starting piece thingy 

import sys
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException

# Run Firefox
firefoxOption = Options()
firefoxOption.add_argument('-headless');
firefoxOption.add_argument('--window-size=1920,1080')
driver = webdriver.Firefox(firefox_options=firefoxOption)
P_PATH = '.\\'
URL = ''

# # # [FOLDER MAKING FACTORY] # # #
# create nested folders
def createFolders():
	global P_PATH
	P_PATH = '.\\'
	pathList = driver.find_elements_by_class_name('breadcrumb-item-text')
	for p in pathList:
		P_PATH += p.text + "\\"
	os.makedirs(P_PATH, exist_ok=True)
	populateFolder()

# Put in the myeet
def populateFolder():
	ProblemStatement()
	ProblemCode()
	InputOutput()

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

#Creates Input and Output files
def InputOutput():
	p_Input = driver.find_element_by_class_name('challenge_sample_input_body').text
	inp = open('{0}/inp.txt'.format(P_PATH), 'w')
	inp.write(p_Input)
	inp.close()

	p_Output = driver.find_element_by_class_name('challenge_sample_output_body').text
	out = open('{0}/out.txt'.format(P_PATH), 'w')
	out.write(p_Output)
	out.close()

# # # [HELPER INTERFACE] # # #
def HelperInterface():
	global P_PATH
	print("'get <url>' => Creates folder for the problem")
	print("'run' => Run the program and check output")
	print("'reset' => Defaults all the file")
	print("'quit' or 'exit' => Exit the program")

	usr_Cmd = ""
	while(usr_Cmd != 'quit' or usr_Cmd != 'exit'):
		usr_Cmd = input(">> ")
		usr_Cmd = usr_Cmd.lower()
		if(usr_Cmd[:3]=="get"):
			if len(usr_Cmd)<=4:
				print("Usage: 'get <url>'")
			else:
				global URL
				URL = usr_Cmd[4:]
				try:
					driver.get(URL)
					try:
						close_btn = driver.find_element_by_class_name('close-icon')
						close_btn.click()
					except:
						pass
					createFolders()
				except WebDriverException:
					print("Wrong Url.")
					
		elif(usr_Cmd == "run" or usr_Cmd== "r"):
			HelperRun()
		elif(usr_Cmd == "reset" or usr_Cmd == "rs" ):
			createFolders()
		elif(usr_Cmd == "quit" or usr_Cmd == "exit" or usr_Cmd == "q"):
			return
		elif(usr_Cmd == "cls"):
			os.system("cls")
		else:
			print("Invalid Command.")

def HelperRun():
	global P_PATH
	lang = P_PATH.split('\\')[2]
	programName = ''.join(ch for ch in P_PATH.split('\\')[-2] if ch.isalnum())
	try:
		r = os.system("Helper.bat {0} {1} \"{2}\"".format(lang, programName, P_PATH))
	except:
		pass

# # # [MAIN] # # #
def main():
	global URL 
	# Check if URL is provided
	if (len(sys.argv) >= 2):
		URL = sys.argv[1]
		driver.get(URL)
		try:
			close_btn = driver.find_element_by_class_name('close-icon')
			close_btn.click()
		except:
			pass
		createFolders()

	HelperInterface()
	driver.close()

if __name__ == "__main__":
	main()
