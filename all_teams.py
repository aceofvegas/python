############ TO DO: MOVES SLOWER THAN DESIRED AND IS STILL BUGGY

import itertools
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
from selenium.common.exceptions import TimeoutException


# date will be doc name
today = date.today()
newpath = '/home/wsb/CSV/MLB/'+str(today)+'/'
if not os.path.exists(newpath):
    os.makedirs(newpath)
########## ad extensions aka adblock ##########
options = webdriver.ChromeOptions()
options.add_extension('/home/wsb/Downloads/uBlock-Origin.crx')

# driver and set wait 
driver = webdriver.Chrome('/home/wsb/Downloads/chromedriver',options = options)
wait = WebDriverWait(driver, 10)
###############################################################################
url = ['https://www.baseball-reference.com/teams/NYY/2022-schedule-scores.shtml']
# Webpage url   
team_list = ['NYY','BAL','TBR','TOR','BOS','MIN','CLE','CHW','DET','KCR','HOU','SEA','TEX','LAA','OAK','NYM','ATL','PHI','MIA','WSN','MIL','STL','CHC','PIT','CIN','LAD','SDP','SFG','ARI','COL']
for x in team_list:
    url = 'https://www.baseball-reference.com/teams/'+str(x)+'/2022-schedule-scores.shtml'
    driver.get(url)


    ########################### count games played to remove future games
    ############################################################## /html/body/div[2]/div[6]/div[4]/div[2]/div/div[1]/table/tbody/tr[3]/td[2]
  
    try:    
        wins = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[4]/div[2]/div/div[1]/table/tbody/tr[3]/td[2]'))).text
        losses = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[4]/div[2]/div/div[1]/table/tbody/tr[3]/td[3]'))).text
        total_games = int(wins)+int(losses)
        gp = int(total_games+2)
        print(str(x)+' has played '+str(total_games)+str(' games'))
###################################################### EXCEPTION BC NOT ALL TEAMS HAVE EXACT SAME XPATH        
    except TimeoutException:
        wins = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[6]/div[4]/div[2]/div/div[1]/table/tbody/tr[3]/td[2]'))).text
        losses = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[6]/div[4]/div[2]/div/div[1]/table/tbody/tr[3]/td[3]'))).text
        total_games = int(wins)+int(losses)
        gp = int(total_games+2)
        print(str(x)+' has played '+str(total_games)+str(' games'))


    ########## GET TO CSV SHIT
    #button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[5]/div[4]/div[1]/div/ul/li[4]/span'))).click()
    #button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[5]/div[4]/div[1]/div/ul/li[4]/span'))).click()

     ############################# THIS BLOCK DESIGNED FOR NYY
    try:    
        a = ActionChains(driver)
        z = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="team_schedule"]/tbody/tr[9]/th')))
        a.move_to_element_with_offset(z,5,5).perform()
    except MoveTargetOutOfBoundsException:
        print('prob working')


        time.sleep(2)
        ########################### HOVERS OVER SHARE & EXPORT
        a = ActionChains(driver)
        ###########################################################'/html/body/div[2]/div[5]/div[5]/div[1]/div/ul/li[1]/span'
        m = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="team_schedule_sh"]/div/ul/li[1]/span')))
        a.move_to_element_with_offset(m,5,5).perform()
        ################## CLICK ON MODIFY EXPORT FROM DROPDOWN
        button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="team_schedule_sh"]/div/ul/li[1]/div/ul/li[1]'))).click()
        button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="team_schedule_sh"]/div/ul/li[1]/div/ul/li[1]'))).click()
        ############### get to actual csv format 
        time.sleep(2)

        ################################ CLICK ON THE GENERATE CSV OPTION
        a = ActionChains(driver)
        m = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="commands_team_schedule"]/div[5]/button[9]')))
        a.move_to_element(m).perform()
        button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commands_team_schedule"]/div[5]/button[9]'))).click()
        button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commands_team_schedule"]/div[5]/button[9]'))).click()
        button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commands_team_schedule"]/div[5]/button[9]'))).click()
        #button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commands_expanded_standings_overall"]/div[5]/button[9]'))).click()



        #/html/body/div[5]/div[2]/form/textarea
        csv_shit = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/form/textarea'))).text

        #csv_shit = driver.find_element_by_xpath('/html/body/div[5]/div[2]/form/textarea').text()
        #print(csv_shit)

        ########################## WRITE TO TEXT THEN CONVERT TO CSV
        with open(newpath+str(x)+str(today)+'.txt', 'w') as f:
            f.write(csv_shit)


        p = Path(newpath+str(x)+str(today)+'.txt')
        p.rename(p.with_suffix('.csv'))


        ############ remove useless lines/clean CSV
        lines = list()
        rownumbers_to_remove= [1,2,3,4]

        with open(newpath+str(x)+str(today)+'.csv', 'r') as read_file:
            reader = csv.reader(read_file)
            for row_number, row in enumerate(reader, start=1):
                if(row_number not in rownumbers_to_remove):
                    lines.append(row)

        with open(newpath+str(x)+str(today)+'.csv', 'w') as write_file:
            writer = csv.writer(write_file)
            writer.writerows(lines)
        for i in range(gp,170):
            lines = list()
            rownumbers_to_remove= [gp]
            with open(newpath+str(x)+str(today)+'.csv', 'r') as read_file:
                reader = csv.reader(read_file)
                for row_number, row in enumerate(reader, start=1):
                    if(row_number not in rownumbers_to_remove):
                        lines.append(row)

            with open(newpath+str(x)+str(today)+'.csv', 'w') as write_file:
                writer = csv.writer(write_file)
                writer.writerows(lines)
        


        print('Saved to /home/wsb/CSV/MLB/'+str(x)+str(today)+'.csv')
        
    
##################### BLOCK DESIGNED FOR BAL
    except TimeoutException:
        try:    
            a = ActionChains(driver)
            z = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[5]/div[2]/table/tbody/tr[9]/th')))
            a.move_to_element_with_offset(z,5,5).perform()
        except TimeoutException:
            try:    ###################### TBR
                a = ActionChains(driver)
                z = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="team_schedule"]/tbody/tr[9]/th')))
                a.move_to_element_with_offset(z,5,5).perform()
            except MoveTargetOutOfBoundsException:
                print('prob working')


                time.sleep(2)
                ########################### HOVERS OVER SHARE & EXPORT
                a = ActionChains(driver)
                ###########################################################'/html/body/div[2]/div[5]/div[5]/div[1]/div/ul/li[1]/span'
                m = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[6]/div[5]/div[1]/div/ul/li[1]/span')))
                a.move_to_element_with_offset(m,5,5).perform()
                ################## CLICK ON MODIFY EXPORT FROM DROPDOWN
                button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[6]/div[5]/div[1]/div/ul/li[1]/div/ul/li[1]/button'))).click()
                button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[6]/div[5]/div[1]/div/ul/li[1]/div/ul/li[1]/button'))).click()
                ############### get to actual csv format 
                time.sleep(2)

                ################################ CLICK ON THE GENERATE CSV OPTION
                a = ActionChains(driver)
                m = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="commands_team_schedule"]/div[5]/button[9]')))
                a.move_to_element(m).perform()
                button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commands_team_schedule"]/div[5]/button[9]'))).click()
                button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commands_team_schedule"]/div[5]/button[9]'))).click()
                button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commands_team_schedule"]/div[5]/button[9]'))).click()
                #button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commands_expanded_standings_overall"]/div[5]/button[9]'))).click()



                #/html/body/div[5]/div[2]/form/textarea
                csv_shit = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/form/textarea'))).text

                #csv_shit = driver.find_element_by_xpath('/html/body/div[5]/div[2]/form/textarea').text()
                #print(csv_shit)

                ########################## WRITE TO TEXT THEN CONVERT TO CSV
                with open(newpath+str(x)+str(today)+'.txt', 'w') as f:
                    f.write(csv_shit)


                p = Path(newpath+str(x)+str(today)+'.txt')
                p.rename(p.with_suffix('.csv'))


                ############ remove useless lines
                lines = list()
                rownumbers_to_remove= [1,2,3,4]

                with open(newpath+str(x)+str(today)+'.csv', 'r') as read_file:
                    reader = csv.reader(read_file)
                    for row_number, row in enumerate(reader, start=1):
                        if(row_number not in rownumbers_to_remove):
                            lines.append(row)

                with open(newpath+str(x)+str(today)+'.csv', 'w') as write_file:
                    writer = csv.writer(write_file)
                    writer.writerows(lines)
                for i in range(gp,170):
                    lines = list()
                    rownumbers_to_remove= [gp]
                    with open(newpath+str(x)+str(today)+'.csv', 'r') as read_file:
                        reader = csv.reader(read_file)
                        for row_number, row in enumerate(reader, start=1):
                            if(row_number not in rownumbers_to_remove):
                                lines.append(row)

                    with open(newpath+str(x)+str(today)+'.csv', 'w') as write_file:
                        writer = csv.writer(write_file)
                        writer.writerows(lines)



                print('Saved to /home/wsb/CSV/MLB/'+str(x)+str(today)+'.csv')
                ############## ADD TO ZIP FILE
                

        except MoveTargetOutOfBoundsException: ########### back to BAL
            print('prob working')


            time.sleep(2)
            ########################### HOVERS OVER SHARE & EXPORT
            a = ActionChains(driver)
            ###########################################################'/html/body/div[2]/div[5]/div[5]/div[1]/div/ul/li[1]/span'
            m = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[5]/div[5]/div[1]/div/ul/li[1]/span')))
            a.move_to_element_with_offset(m,5,5).perform()
            ################## CLICK ON MODIFY EXPORT FROM DROPDOWN
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[5]/div[5]/div[1]/div/ul/li[1]/div/ul/li[1]/button'))).click()
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[5]/div[5]/div[1]/div/ul/li[1]/div/ul/li[1]/button'))).click()
            ############### get to actual csv format 
            time.sleep(2)

            ################################ CLICK ON THE GENERATE CSV OPTION
            a = ActionChains(driver)
            m = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="commands_team_schedule"]/div[5]/button[9]')))
            a.move_to_element(m).perform()
            button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commands_team_schedule"]/div[5]/button[9]'))).click()
            button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commands_team_schedule"]/div[5]/button[9]'))).click()
            button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commands_team_schedule"]/div[5]/button[9]'))).click()
            #button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="commands_expanded_standings_overall"]/div[5]/button[9]'))).click()



            #/html/body/div[5]/div[2]/form/textarea
            csv_shit = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/form/textarea'))).text

            #csv_shit = driver.find_element_by_xpath('/html/body/div[5]/div[2]/form/textarea').text()
            #print(csv_shit)

            ########################## WRITE TO TEXT THEN CONVERT TO CSV
            with open(newpath+str(x)+str(today)+'.txt', 'w') as f:
                f.write(csv_shit)


            p = Path(newpath+str(x)+str(today)+'.txt')
            p.rename(p.with_suffix('.csv'))


            ############ remove useless lines
            lines = list()
            rownumbers_to_remove= [1,2,3,4]

            with open(newpath+str(x)+str(today)+'.csv', 'r') as read_file:
                reader = csv.reader(read_file)
                for row_number, row in enumerate(reader, start=1):
                    if(row_number not in rownumbers_to_remove):
                        lines.append(row)

            with open(newpath+str(x)+str(today)+'.csv', 'w') as write_file:
                writer = csv.writer(write_file)
                writer.writerows(lines)
            for i in range(gp,170):
                lines = list()
                rownumbers_to_remove= [gp]
                with open(newpath+str(x)+str(today)+'.csv', 'r') as read_file:
                    reader = csv.reader(read_file)
                    for row_number, row in enumerate(reader, start=1):
                        if(row_number not in rownumbers_to_remove):
                            lines.append(row)

                with open(newpath+str(x)+str(today)+'.csv', 'w') as write_file:
                    writer = csv.writer(write_file)
                    writer.writerows(lines)


            print('Saved to /home/wsb/CSV/MLB/'+str(x)+str(today)+'.csv')
           
for x in team_list:
    p = Path(newpath+str(x)+str(today)+'.csv')           
    x = open(p)
    s = x.read().replace('Gm#', 'Gm' ) 
    x.close()
    x = open(p,'w')
    x.write(s)
    x.close()
    with zipfile.ZipFile(str(today)+'.zip', 'a') as myzip:
        myzip.write(p)
print('Fixed CSV files and saved to zip: '+str(today)+'.zip')
print('Complete: closing script now')
driver.close()



