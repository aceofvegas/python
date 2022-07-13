############ TO DO: 


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import csv
from datetime import date
from pathlib import Path
import os 
import zipfile
import time
################################
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import MoveTargetOutOfBoundsException

# date will be doc name
today = date.today()
########## ad extensions aka adblock ##########
options = webdriver.ChromeOptions()
options.add_extension('/home/wsb/Downloads/uBlock-Origin.crx')

# driver and set wait 
driver = webdriver.Chrome('/home/wsb/Downloads/chromedriver',options = options)
wait = WebDriverWait(driver, 30)
###############################################################################

# Webpage url   


url = 'https://www.baseball-reference.com/leagues/MLB-standings.shtml'

driver.get(url)

########## GET TO CSV SHIT
#button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[5]/div[4]/div[1]/div/ul/li[4]/span'))).click()
#button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[5]/div[4]/div[1]/div/ul/li[4]/span'))).click()

try:    
    a = ActionChains(driver)
    z = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[4]/div[4]/table/tbody/tr[10]/td[1]/a')))
    a.move_to_element_with_offset(z,5,5).perform()
except MoveTargetOutOfBoundsException:
    print('prob working')


    time.sleep(2)
    ########################### HOVERS OVER SHARE & EXPORT
    a = ActionChains(driver)
    m = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[4]/div[1]/div/ul/li[2]/span')))
    a.move_to_element_with_offset(m,5,5).perform()
    ################## CLICK ON MODIFY EXPORT FROM DROPDOWN
    button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[5]/div[4]/div[1]/div/ul/li[2]/div/ul/li[1]/button'))).click()
    button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[5]/div[4]/div[1]/div/ul/li[2]/div/ul/li[1]/button'))).click()
    ############### get to actual csv format 
    time.sleep(5)

    ################################ CLICK ON THE GENERATE CSV OPTION
    a = ActionChains(driver)
    m = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="commands_expanded_standings_overall"]/div[5]/button[9]')))
    a.move_to_element(m).perform()
    button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commands_expanded_standings_overall"]/div[5]/button[9]'))).click()
    button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commands_expanded_standings_overall"]/div[5]/button[9]'))).click()
    button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commands_expanded_standings_overall"]/div[5]/button[9]'))).click()
    #button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commands_expanded_standings_overall"]/div[5]/button[9]'))).click()



    #/html/body/div[5]/div[2]/form/textarea
    csv_shit = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/form/textarea'))).text

    #csv_shit = driver.find_element_by_xpath('/html/body/div[5]/div[2]/form/textarea').text()
    #print(csv_shit)

    ########################## WRITE TO TEXT THEN CONVERT TO CSV
    with open('/home/wsb/CSV/MLB/standings.txt', 'w') as f:
        f.write(csv_shit)


    p = Path('/home/wsb/CSV/MLB/standings.txt')
    p.rename(p.with_suffix('.csv'))


    ############ remove useless lines
    lines = list()
    rownumbers_to_remove= [1,2,3,4,36,37,38,39]

    with open('/home/wsb/CSV/MLB/standings.csv', 'r') as read_file:
        reader = csv.reader(read_file)
        for row_number, row in enumerate(reader, start=1):
            if(row_number not in rownumbers_to_remove):
                lines.append(row)

    with open('/home/wsb/CSV/MLB/standings.csv', 'w') as write_file:
        writer = csv.writer(write_file)
        writer.writerows(lines)

    print('Saved to /home/wsb/CSV/MLB/standings.csv')
    print('Closing out script')

    driver.close()



