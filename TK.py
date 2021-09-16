#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 12:02:24 2021

@author: williamsheehan
"""
import tkinter as tk
#from tkinter import *
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import geckodriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def get_email(url, pages, output_name):
    geckodriver_autoinstaller.install()
    profile = webdriver.FirefoxProfile(
    #'/Users/williamsheehan/Library/Application Support/Firefox/Profiles/vb9qi9v8.default'
    )

    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)
    profile.update_preferences()
    desired = DesiredCapabilities.FIREFOX
    
    binary = FirefoxBinary('/Applications/Firefox.app/Contents/MacOS/firefox')
    driver = webdriver.Firefox(
        #executable_path = '/Users/williamsheehan/anaconda3/bin/geckodriver',
                              firefox_profile=profile,
                              desired_capabilities=desired,
                              firefox_binary=binary,
                              log_path='/tmp/geckodriver.log')

    def check_exists_by_xpath(xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True
    def check_exists_by_css(css):
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.zp-button:nth-child(2) > div:nth-child(2)")))
        except TimeoutException:
            return False
        return True
    def check_exists_by_id(ID):
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, ID)))
        except TimeoutException:
            return False
        return True
    
    def recruiter_href(url, pages):
        pages = int(pages)
        names = {}
        driver.get(url)
        if check_exists_by_id('username'):
            print('logging in')
            email_input = driver.find_element_by_id('username')
            email_input.send_keys('cgomez@spiritmco.com')
            pw_input = driver.find_element_by_id('password')
            pw_input.send_keys('Wilson2021!')
            driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[3]/button').click()
        print('loading...')
        time.sleep(8)
        
        pages_remaining = True
        page_counter = 1
        while pages_remaining:
            print('loading page {} of results'.format(page_counter))
            time.sleep(5)
            body = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            ol = body.find_elements_by_tag_name('ol')[0]
            lis = ol.find_elements_by_tag_name('li')
            for l in lis:
                try:
                    a = l.find_element_by_tag_name('a')
                    name = a.text
                    href = a.get_attribute('href')
                    names[name] = href
                except NoSuchElementException:
                    continue
            if page_counter == 1:
                xpath = '/html/body/div[2]/div[6]/div/div[2]/div[1]/div[1]/span/section/span/div/form/div[1]/div[2]/span/a'
            else:
                xpath = '/html/body/div[2]/div[6]/div/div[2]/div[1]/div[1]/span/section/span/div/form/div[1]/div[2]/span/a[2]'
            next_page = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH, xpath)))
            next_page.click()    
            page_counter +=1
            if page_counter > pages:
                pages_remaining = False
                break;
        return names
    
    
    def recruiter_info(persons):
        dictionary = {}
        for person in persons:
            try:
                link = persons[person]
                person = person.split(', ')[0]
                person = person.split('- ')[0]
                driver.get(link)
                print("loading {}'s profile".format(person))
                button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[6]/div/div[2]/main/div/span/div/div/header/section/div[1]/div[1]/div[2]/span/button')))
                button.click()
                xp = '/html/body/div[2]/aside[2]/div[1]/div[1]/div/a'
                a = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xp)))
                public_profile = a.get_attribute('href')
                
                try:
                    xp = '/html/body/div[2]/div[6]/div/div[2]/main/div/span/div/div/header/section/div[1]/div[1]/section/div/div[2]/div[2]/div'
                    loc = driver.find_element_by_xpath(xp).text
                except NoSuchElementException:
                    xp = '/html/body/div[2]/div[6]/div/div[2]/main/div/span/div/div/header/section/div[1]/div[1]/section/div/div[2]/div[3]/div'
                    loc = driver.find_element_by_xpath(xp).text
                    
                
                background_card = driver.find_element_by_xpath('/html/body/div[2]/div[6]/div/div[2]/main/div/span/div/div/div[2]/div/section[2]')
                jobs = background_card.find_elements_by_tag_name('div')[0].find_elements_by_tag_name('li')
                current = jobs[0]
                dds = current.find_elements_by_tag_name('dd')
                if len(dds) > 0:
                    position = dds[0].find_element_by_tag_name('a').text
                    try:
                        company = dds[1].find_element_by_tag_name('a').text.split(' •')[0]
                    except NoSuchElementException:
                        try:
                            company = current.find_element_by_tag_name('strong').text.split(' •')[0]
                        except NoSuchElementException:
                             company = dds[1].text.split(' •')[0]
                        
                    try: 
                        duration = dds[2].find_element_by_tag_name('span').text
                    except NoSuchElementException:
                        duration = dds[1].find_element_by_tag_name('span').text
                
                school = ''
                degree = ''
                years = ''
                field_of_study = ''
                job_divs = background_card.find_elements_by_tag_name('div')[0].find_elements_by_tag_name('div')
                try:
                    edu = background_card.find_elements_by_tag_name('div')[len(job_divs) + 1].find_elements_by_tag_name('li')
                    recent = edu[0]
                    ddss = recent.find_elements_by_tag_name('dd')
                    school = ddss[0].text
                    for d in ddss:
                        if ' – ' in d.text:
                            years = d.text
                            
                        if 'Degree name' in d.text:
                            degree = d.text.split('Degree name\n')[-1]
                            if 'Field of study' in degree:
                                degree = degree.split('Field of study')[0].split(' •')[0]
                    
                        if 'Field of study' in d.text:
                            field_of_study = d.text.split('Field of study\n')[-1].split(' •')[0]
                except IndexError:
                    pass
                
                dictionary[person] = {'Location': loc, 'Current Position': position, 'Current Company': company,
                                           'Employment Dates': duration, 'Most Recent Education': school, 'Years Attended': years,
                                           'Degree': degree,'Field of Study': field_of_study, 'Public Profile': public_profile}
            except Exception as e:
                print(e)
                continue
              
        return dictionary
    

    def search_person(field, option):
        field.send_keys(option)
        try:
            person = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div/div/div/div/div[2]/div/table/tbody/tr')))
            href = person.find_element_by_class_name('zp_yJfMM').find_element_by_class_name('zp_1sGdg').find_element_by_class_name('zp_EqOJn').find_element_by_class_name('zp_PrhFA').find_element_by_tag_name('a').get_attribute('href')
            return href
        except:
            href = None
    
        
    def search_ap(url): 
        driver.get(url)
        time.sleep(2)
        try:
            person = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div/div/div/div/div[2]/div/table/tbody/tr')))
            href = person.find_element_by_class_name('zp_yJfMM').find_element_by_class_name('zp_1sGdg').find_element_by_class_name('zp_EqOJn').find_element_by_class_name('zp_PrhFA').find_element_by_tag_name('a').get_attribute('href')
        except:
            href = None
        return href
    
    
    def apollo_href(in_dict):
        
        url = 'https://app.apollo.io/#/companies?prospectedByCurrentTeam[]=no&finderViewId=5a205be19a57e40c095e1d5f&page=1'
        driver.get(url)
        time.sleep(6)
        if check_exists_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/form/div[1]/div') == True:
            print('gotta log in')
            google_login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#provider-mounter > div > div.zp_2Pnik > div.zp_2YB95 > div > div.zp_1QN2s > div > div.zp_p7Ra4.zp_2ZLGm > div > form > div:nth-child(1) > div")))
            google_login.click()
            try:
                email = driver.find_element_by_id("identifierId")
                email.send_keys('wsheehan.spiritmco@gmail.com')
                next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#identifierNext > div > button > span")))
                next_button.click()
                bypass = False
            except NoSuchElementException:
                auto_login = True
                bypass = False
                print('auto login')
        
            if bypass == True:
                ppl_css = 'a.zp_2EIcj:nth-child(1)'
                people = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, ppl_css)))
                people.click()
            if auto_login == True:
                search = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "sidebar-nav-prospect-search")))
                search.click()
                ppl_css = 'a.zp_2EIcj:nth-child(1)'
                people = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, ppl_css)))
                people.click()
        else:
            search = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "sidebar-nav-prospect-search")))
            search.click()
            ppl_css = 'a.zp_2EIcj:nth-child(1)'
            people = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ppl_css)))
            people.click()

        
        for name in in_dict:
            data = in_dict[name]
            company = data['Current Company']
            location = data['Location'].split('Greater ')[-1]
            location = location.split(',')[0]
            position = data['Current Position']
            first_name = name.split(' ')[0]
            last_name = name.split(' ')[-1]
            
            query_str = 'https://app.apollo.io/#/people?finderViewId=5a205be19a57e40c095e1d5f&qKeywords={first}%20{last}%20{flex}&page=1'
            
            href = None
            u = query_str.format(first=first_name, last = last_name, flex=company)
            print(u)
            href = search_ap(u)
            if href is None:
                u = query_str.format(first=first_name, last = last_name, flex=location)
                href = search_ap(u)
                if href is None:
                     u = query_str.format(first=first_name, last = last_name, flex=position)
                     href = search_ap(u)
                     if href is None:
                         u = 'https://app.apollo.io/#/people?finderViewId=5a205be19a57e40c095e1d5f&qKeywords={first}%20{flex}&page=1'.format(first=first_name,flex=company)
                         href = search_ap(u)
            in_dict[name]['Apollo Link'] = href
            time.sleep(3)
            
        return in_dict
    
    def save_to_file(dictionary, output_name):
        dataframe = pd.DataFrame(dictionary).T
        filename = output_name + '.csv'
        dataframe.to_csv(filename)  
        
    out_dict = {}
    
    names = recruiter_href(url, pages)
    #names = {'Kyle Allen': 'https://www.linkedin.com/talent/profile/AEMAAAi0Z8UBLk82H0pv0HPqlWu0nvWM5y-UJmQ', 'Helen Wainwright, SHRM-SCP': 'https://www.linkedin.com/talent/profile/AEMAAAEzF8IBsJixmH1fSBtstzRFcuLDXm-P3tA', 'J.D. Pohutsky': 'https://www.linkedin.com/talent/profile/AEMAABKNJj4B5a1RIpHSgtJqV97KogYO6hUonIo', 'Kristine Phisayavong': 'https://www.linkedin.com/talent/profile/AEMAAAzU8zwBFgvBn5z3katqs5bJ02A88ZwWc3s', 'Mike Snoy': 'https://www.linkedin.com/talent/profile/AEMAAA7F1zoB-gl3-2-ga_cSWCOiZg6zQcrsYSQ', 'Vikki Carter': 'https://www.linkedin.com/talent/profile/AEMAAADh2N8BPi-nYQ4NNxNBGia5-wBWEV8aWY0', 'Julie Angelos': 'https://www.linkedin.com/talent/profile/AEMAAAGNjfUB2IM_zVvW4KlBUlGuKFEhaW-KbX4', 'Joe Grilli': 'https://www.linkedin.com/talent/profile/AEMAAChtmu4BDbQ9aMLBDO4brMKk2Yqj5w3KeM0', 'Hally Kocur': 'https://www.linkedin.com/talent/profile/AEMAACHYtBcB7onqLItaEKtdv5dRZuhcmsHNFAw', 'Melissa Mushlin': 'https://www.linkedin.com/talent/profile/AEMAAABH_5QBCCcLPH54tOrI7hEQbLlL_F0sLlo', 'Michael Sweetser': 'https://www.linkedin.com/talent/profile/AEMAAAaGnzcBLlPn-eYyRzItGMoGr3yXe8aysrU', 'Julie Keiper, CPMSM': 'https://www.linkedin.com/talent/profile/AEMAAAC9LBkB11mfoIK0iqkezeamkNWQO0hHEQw', 'Bradley Smith': 'https://www.linkedin.com/talent/profile/AEMAAASBWKMBMw9NI0w0k287nz1rKSln55Ie-mk', 'Kara Stead, SHRM-CP': 'https://www.linkedin.com/talent/profile/AEMAAAMcTAgBnaib5OeKFl1U2CJhDuu5X4toY38', 'James Heinlen- MBA': 'https://www.linkedin.com/talent/profile/AEMAAARacMkB7TGkBYvlkDF_hPpKPytKLXXVvlw', 'Colette Colburn': 'https://www.linkedin.com/talent/profile/AEMAAAD-8ywBl7tsB2Rl2pDI2NrOr2HC1Y_XCmE', 'Brendan Dee': 'https://www.linkedin.com/talent/profile/AEMAAA73UDUBHknmg8P4xvnMxkm31LWVDxXvgFk', 'Robyn Goode, PHR': 'https://www.linkedin.com/talent/profile/AEMAAAFYNCkBMKua--vBB4HyAaQuHpkxOkEea0g', 'Krushita Shah': 'https://www.linkedin.com/talent/profile/AEMAABzm0XABwsgYQ7C-HG1pRycC6XeBRyod-8M', 'Harshini Reddy': 'https://www.linkedin.com/talent/profile/AEMAABNnRCUB62KSlBpo-_mxqJtVfrKq9BjM1jY', 'James Taylor': 'https://www.linkedin.com/talent/profile/AEMAABwwf-AB7y8SLmtisMqOcaFT9B21fA43oKo', 'Kenya Howard, MBA': 'https://www.linkedin.com/talent/profile/AEMAAAeK1MoBq86uNV2RHyef_JbfzYr6iiWNcak', 'William C. Bell, MHA': 'https://www.linkedin.com/talent/profile/AEMAAA0zZfMBZ6d7L1wuwSxKVnYGzff5BD51i9U', 'Brittany Lett': 'https://www.linkedin.com/talent/profile/AEMAAAFua5cBkqB4OIn3ktcFjggq8dPb4VPHXMA', 'Austin Laughner, PMP, CSM': 'https://www.linkedin.com/talent/profile/AEMAAAOAZEUBdsgHutrUvVfdwUODZyfwEz1W_XQ'}
    #names = {'Kyle Allen': 'https://www.linkedin.com/talent/profile/AEMAAAi0Z8UBLk82H0pv0HPqlWu0nvWM5y-UJmQ', 'Helen Wainwright, SHRM-SCP': 'https://www.linkedin.com/talent/profile/AEMAAAEzF8IBsJixmH1fSBtstzRFcuLDXm-P3tA', 'J.D. Pohutsky': 'https://www.linkedin.com/talent/profile/AEMAABKNJj4B5a1RIpHSgtJqV97KogYO6hUonIo', 'Kristine Phisayavong': 'https://www.linkedin.com/talent/profile/AEMAAAzU8zwBFgvBn5z3katqs5bJ02A88ZwWc3s', 'Mike Snoy': 'https://www.linkedin.com/talent/profile/AEMAAA7F1zoB-gl3-2-ga_cSWCOiZg6zQcrsYSQ', 'Vikki Carter': 'https://www.linkedin.com/talent/profile/AEMAAADh2N8BPi-nYQ4NNxNBGia5-wBWEV8aWY0', 'Julie Angelos': 'https://www.linkedin.com/talent/profile/AEMAAAGNjfUB2IM_zVvW4KlBUlGuKFEhaW-KbX4', 'Joe Grilli': 'https://www.linkedin.com/talent/profile/AEMAAChtmu4BDbQ9aMLBDO4brMKk2Yqj5w3KeM0', 'Hally Kocur': 'https://www.linkedin.com/talent/profile/AEMAACHYtBcB7onqLItaEKtdv5dRZuhcmsHNFAw', 'Melissa Mushlin': 'https://www.linkedin.com/talent/profile/AEMAAABH_5QBCCcLPH54tOrI7hEQbLlL_F0sLlo', 'Michael Sweetser': 'https://www.linkedin.com/talent/profile/AEMAAAaGnzcBLlPn-eYyRzItGMoGr3yXe8aysrU', 'Julie Keiper, CPMSM': 'https://www.linkedin.com/talent/profile/AEMAAAC9LBkB11mfoIK0iqkezeamkNWQO0hHEQw', 'Brendan Dee': 'https://www.linkedin.com/talent/profile/AEMAAA73UDUBHknmg8P4xvnMxkm31LWVDxXvgFk', 'Kara Stead, SHRM-CP': 'https://www.linkedin.com/talent/profile/AEMAAAMcTAgBnaib5OeKFl1U2CJhDuu5X4toY38', 'Bradley Smith': 'https://www.linkedin.com/talent/profile/AEMAAASBWKMBMw9NI0w0k287nz1rKSln55Ie-mk', 'Colette Colburn': 'https://www.linkedin.com/talent/profile/AEMAAAD-8ywBl7tsB2Rl2pDI2NrOr2HC1Y_XCmE', 'James Taylor': 'https://www.linkedin.com/talent/profile/AEMAABwwf-AB7y8SLmtisMqOcaFT9B21fA43oKo', 'Erika Swift': 'https://www.linkedin.com/talent/profile/AEMAABGJUfUBEQ-6Cw6vdByHr32rsWJbLCx04PM', 'James Heinlen- MBA': 'https://www.linkedin.com/talent/profile/AEMAAARacMkB7TGkBYvlkDF_hPpKPytKLXXVvlw', 'Shannon Davis': 'https://www.linkedin.com/talent/profile/AEMAAAetuzoB5RYtx2rpBbAU8uOnzgP_rPYvJfs', 'Krushita Shah': 'https://www.linkedin.com/talent/profile/AEMAABzm0XABwsgYQ7C-HG1pRycC6XeBRyod-8M', 'Brittany Lett': 'https://www.linkedin.com/talent/profile/AEMAAAFua5cBkqB4OIn3ktcFjggq8dPb4VPHXMA', 'William C. Bell, MHA': 'https://www.linkedin.com/talent/profile/AEMAAA0zZfMBZ6d7L1wuwSxKVnYGzff5BD51i9U', 'Robyn Goode, PHR': 'https://www.linkedin.com/talent/profile/AEMAAAFYNCkBMKua--vBB4HyAaQuHpkxOkEea0g', "Benjamin O'Shea": 'https://www.linkedin.com/talent/profile/AEMAABHsONgBAs3c6TOh9Kv8BaSFKjoB9wCtGRk', 'Taylor Clemmer, CHPCA, FACHE': 'https://www.linkedin.com/talent/profile/AEMAAAJSf8sBPDeKaaxV7ncWpuG4o-attuHi-k4', 'Austin Laughner, PMP, CSM': 'https://www.linkedin.com/talent/profile/AEMAAAOAZEUBdsgHutrUvVfdwUODZyfwEz1W_XQ', 'Harshini Reddy': 'https://www.linkedin.com/talent/profile/AEMAABNnRCUB62KSlBpo-_mxqJtVfrKq9BjM1jY', 'Keith Kirby': 'https://www.linkedin.com/talent/profile/AEMAAAbbuQUBYDKPS_UH4VDDoIdUona6_jgytnY', 'Claudia Soltys, SHRM-CP (She,Her)': 'https://www.linkedin.com/talent/profile/AEMAAAKJNh8BSUgnwr3u9ZBmptVl4zK32NMeUbQ', 'Scott Kagan': 'https://www.linkedin.com/talent/profile/AEMAAAE01LUBL2lU4eKhY3kfTvLNlQN0TSLuJKk', 'Jennifer Bruns, MBA, SPHR': 'https://www.linkedin.com/talent/profile/AEMAAAOZ7QABMggC6pDhv7bVFgVeNA2wiiERaQY', 'Matthew V. Baker M.S.': 'https://www.linkedin.com/talent/profile/AEMAAApHk90BfbeeItBlzLOXWS6DsqVNhBdhiIo', 'Venus Brady': 'https://www.linkedin.com/talent/profile/AEMAAAB85uoB95PIl9B-BmyjKwF62AIjoxKZ10I', 'Daniel Esquibel': 'https://www.linkedin.com/talent/profile/AEMAAADngP4BfQoBL-_AQ3hiprV_LDKmlg7xYbM', 'Karen Douglas': 'https://www.linkedin.com/talent/profile/AEMAAADdnYABCvQ4KrX8Rqh6pZtYjmbl5BNHDNY', 'Mario L.': 'https://www.linkedin.com/talent/profile/AEMAAAJOn3MB8LTZnMV38TM7fZX-DsMQYL2pr5E', 'Heather Williams': 'https://www.linkedin.com/talent/profile/AEMAABQc6uoBFHUcZ8fxk9viegaivaFbJyz7pNk', 'Slade Burkeen': 'https://www.linkedin.com/talent/profile/AEMAACIAF34Bb-C6UCR5gaCR6oTEYDdg2FUP0dg', 'Stephanie Mears': 'https://www.linkedin.com/talent/profile/AEMAAAMhlnsB3AqZVbLIZbp8GAq7mFuAeEb83gE', 'Kenya Howard, MBA': 'https://www.linkedin.com/talent/profile/AEMAAAeK1MoBq86uNV2RHyef_JbfzYr6iiWNcak', 'Katherine Lutz, MS': 'https://www.linkedin.com/talent/profile/AEMAAAD1WioBiHTPOH1EtF1MsPS360LkbIvQlao', 'Thurston Stephens': 'https://www.linkedin.com/talent/profile/AEMAAA2TRQUBlK_J9Z4MPC1_iGRMthKvDWhgWD0', 'Nichelle Gibbs, PHR': 'https://www.linkedin.com/talent/profile/AEMAAAz908kBMGUTTy3ZeDTqWoiq3TxkybRyobc', 'Richard Winters, MBA, SPHR': 'https://www.linkedin.com/talent/profile/AEMAAAGeImkBaoOKl5Hhg0vWvVYQlpxXv_MExJA', 'Kacie Moody': 'https://www.linkedin.com/talent/profile/AEMAAAttDoUBX3Gb5pXHPg7nWSuZO6kGU2JHnzw', 'Timothy Chadwick': 'https://www.linkedin.com/talent/profile/AEMAACJUllwBUOYIVzVgMqV-uzliglEQhY5o970', 'Britta Nally, M.S.': 'https://www.linkedin.com/talent/profile/AEMAAA95VRYBHmbfV4iUA2lGcrKVns4Lq1OqPBY', 'Rob Adhikari MBA, MS': 'https://www.linkedin.com/talent/profile/AEMAAAHpiAsBs3klkZLb6tqPbhWlmmREyRQnUag', 'Adrian Castro': 'https://www.linkedin.com/talent/profile/AEMAAC-FU9IBWN5ccML8-I5lv_1IkJauO8sg5RM'}
    dict_less_apollo = recruiter_info(names)
    #print('dict less apollo: {}'.format(len(dict_less_apollo)))
    # dict_less_apollo = {'Kyle Allen': {'Location': 'Dallas-Fort Worth Metroplex', 'Current Position': 'Regional Business Development Manager', 'Current Company': 'Sound Physicians', 'Employment Dates': 'Oct 2014 – Present', 'Most Recent Education': '', 'Years Attended': '', 'Degree': '', 'Field of Study': '', 'Public Profile': 'https://www.linkedin.com/in/kyle-allen-405aaa40'}, 'Helen Wainwright': {'Location': 'Sacramento, California, United States', 'Current Position': 'Regional Business Development Manager', 'Current Company': 'Sound Physicians', 'Employment Dates': 'Oct 2014 – Present', 'Most Recent Education': '', 'Years Attended': '', 'Degree': '', 'Field of Study': '', 'Public Profile': 'https://www.linkedin.com/in/helen-wainwright-shrm-scp-9428a66'}, 'J.D. Pohutsky': {'Location': 'Fort Lauderdale, Florida, United States', 'Current Position': 'Territory Manager - Advanced Endoscopic Technologies', 'Current Company': 'CONMED Corporation', 'Employment Dates': 'Mar 2020 – Present', 'Most Recent Education': 'University of Mississippi', 'Years Attended': '2010 – 2016', 'Degree': 'Bachelor of Science in Criminal Justice', 'Field of Study': 'Emphasis - Homeland Security', 'Public Profile': 'https://www.linkedin.com/in/j-d-pohutsky-a7a29788'}, 'Kristine Phisayavong': {'Location': 'Orange County, California, United States', 'Current Position': 'Territory Sales Manager', 'Current Company': 'Benco Dental', 'Employment Dates': 'Apr 2019 – Jun 2021', 'Most Recent Education': 'Orange Coast College', 'Years Attended': '1987 – 1992', 'Degree': 'Associate of Arts - AA', 'Field of Study': 'Business and Personal/Financial Services Marketing Operations', 'Public Profile': 'https://www.linkedin.com/in/kristine-phisayavong-93812060'}, 'Mike Snoy': {'Location': 'Ogden, Utah, United States', 'Current Position': 'Market Sales Manager', 'Current Company': 'Center for Diagnostic Imaging (CDI)', 'Employment Dates': 'Oct 2020 – Present', 'Most Recent Education': 'Weber State University', 'Years Attended': '2006 – 2010', 'Degree': 'Technical Sales (B.S.)', 'Field of Study': 'Sales, Distribution, and Marketing Operations, General', 'Public Profile': 'https://www.linkedin.com/in/mikesnoy'}, 'Vikki Carter': {'Location': 'Nashville, Tennessee, United States', 'Current Position': 'Regional Business Development Manager', 'Current Company': 'Sound Physicians', 'Employment Dates': 'May 2020 – Present', 'Most Recent Education': 'Western Kentucky University', 'Years Attended': '', 'Degree': 'BA', 'Field of Study': 'Advertising', 'Public Profile': 'https://www.linkedin.com/in/vikkiecarter'}, 'Julie Angelos': {'Location': 'Santa Barbara County, California, United States', 'Current Position': 'Professional Sales Representative', 'Current Company': 'Takeda', 'Employment Dates': 'Sep 2018 – Present', 'Most Recent Education': 'Westmont College', 'Years Attended': '2000 – 2003', 'Degree': 'BA', 'Field of Study': 'Social Science, Business', 'Public Profile': 'https://www.linkedin.com/in/julie-angelos-7598858'}, 'Joe Grilli': {'Location': 'Bloomfield, New Jersey, United States', 'Current Position': 'Client Services Manager', 'Current Company': '365 Health Services, LLC', 'Employment Dates': 'Sep 2020 – Present', 'Most Recent Education': 'Rowan University', 'Years Attended': '2016 – 2020', 'Degree': '3.5 years', 'Field of Study': 'Marketing', 'Public Profile': 'https://www.linkedin.com/in/joe-grilli'}, 'Hally Kocur': {'Location': 'Estero, Florida, United States', 'Current Position': 'Digital Marketing Manager', 'Current Company': 'GenesisCare', 'Employment Dates': 'Sep 2020 – Present', 'Most Recent Education': 'Florida Gulf Coast University', 'Years Attended': '2012 – 2013', 'Degree': 'Bachelor of Arts (B.A.)', 'Field of Study': 'Communication, General', 'Public Profile': 'https://www.linkedin.com/in/hally-kocur-a9b20813a'}, 'Melissa Mushlin': {'Location': 'Greater St. Louis', 'Current Position': 'Senior Business Development Manager', 'Current Company': 'Cross Country Healthcare', 'Employment Dates': '2014 – Present', 'Most Recent Education': 'Way of Life Seminary', 'Years Attended': '', 'Degree': "Bachelor's Degree", 'Field of Study': 'Christian Education', 'Public Profile': 'https://www.linkedin.com/in/melissamushlin'}, 'Michael Sweetser': {'Location': 'Greater Tampa Bay Area', 'Current Position': 'Manager of Broker Sales', 'Current Company': 'Teladoc Health', 'Employment Dates': 'Feb 2020 – Present', 'Most Recent Education': 'Wake Forest University', 'Years Attended': '2009 – 2013', 'Degree': 'Bachelor of Arts (B.A.)', 'Field of Study': 'History & Political Science', 'Public Profile': 'https://www.linkedin.com/in/michael-sweetser-a737bb30'}, 'Julie Keiper': {'Location': 'Waynesville, North Carolina, United States', 'Current Position': 'Provider Account Executive II /Region 1 Lead/Tribal Liaison', 'Current Company': 'AmeriHealth Caritas', 'Employment Dates': 'Jun 2019 – Present', 'Most Recent Education': 'University of Minnesota-Duluth', 'Years Attended': '', 'Degree': 'Bachelor of Arts', 'Field of Study': 'Business / Psychology', 'Public Profile': 'https://www.linkedin.com/in/jakeiper'}, 'Brendan Dee': {'Location': 'North Reading, Massachusetts, United States', 'Current Position': 'Territory Sales Manager', 'Current Company': 'Philips', 'Employment Dates': 'Nov 2019 – Present', 'Most Recent Education': 'University of Massachusetts, Amherst', 'Years Attended': '', 'Degree': 'Bachelor of Arts (B.A.)', 'Field of Study': 'Communications', 'Public Profile': 'https://www.linkedin.com/in/brendan-dee-13110a70'}, 'Kara Stead': {'Location': 'Woodbridge, Virginia, United States', 'Current Position': 'Human Resources Business Partner', 'Current Company': 'Mary Washington Healthcare', 'Employment Dates': 'Nov 2019 – Present', 'Most Recent Education': 'Goucher College', 'Years Attended': '', 'Degree': "Bachelor's degree", 'Field of Study': 'English (Writing)', 'Public Profile': 'https://www.linkedin.com/in/kara-stead-shrm-cp-37458815'}, 'Bradley Smith': {'Location': 'Nashville Metropolitan Area', 'Current Position': 'Regional Sales Manager', 'Current Company': 'Fresenius Medical Care North America', 'Employment Dates': 'Aug 2020 – Present', 'Most Recent Education': 'Indiana University Bloomington', 'Years Attended': '2000 – 2003', 'Degree': 'Bachelor of Arts', 'Field of Study': 'History and Mathematics', 'Public Profile': 'https://www.linkedin.com/in/bradley-smith-88339121'}, 'Colette Colburn': {'Location': 'Seattle, Washington, United States', 'Current Position': 'Program Manager, Strategic Accounts', 'Current Company': 'AMN Healthcare', 'Employment Dates': 'Feb 2019 – Present', 'Most Recent Education': 'Seattle University', 'Years Attended': '1986 – 1991', 'Degree': 'Bachelor of Arts (B.A.)', 'Field of Study': 'History and French', 'Public Profile': 'https://www.linkedin.com/in/colettecolburn'}, 'James Taylor': {'Location': 'Boca Raton, Florida, United States', 'Current Position': 'Regional Sales Manager, Strategic Accounts - Orthopedics', 'Current Company': 'Modernizing Medicine', 'Employment Dates': 'Jan 2021 – Present', 'Most Recent Education': 'Boston College', 'Years Attended': '2013 – 2017', 'Degree': 'Bachelor of Arts (B.A.)', 'Field of Study': 'Economics', 'Public Profile': 'https://www.linkedin.com/in/james-taylor-514478112'}, 'Erika Swift': {'Location': 'Orange County, California, United States', 'Current Position': 'Senior Clinical Manager', 'Current Company': 'naviHealth', 'Employment Dates': 'Feb 2014 – Present', 'Most Recent Education': 'Northwestern University', 'Years Attended': '', 'Degree': 'Master of Science - MS', 'Field of Study': 'Health Analytics', 'Public Profile': 'https://www.linkedin.com/in/erika-swift-75964582'}, 'James Heinlen': {'Location': 'Phoenix, Arizona, United States', 'Current Position': 'Call Center Manager', 'Current Company': 'Dignity Health', 'Employment Dates': 'Mar 2018 – Present', 'Most Recent Education': 'Ashford University', 'Years Attended': '2018 – 2020', 'Degree': 'Master of Business Administration - MBA', 'Field of Study': 'Organizational Leadership', 'Public Profile': 'https://www.linkedin.com/in/james-heinlen-mba-23556220'}, 'Shannon Davis': {'Location': 'Los Angeles Metropolitan Area', 'Current Position': 'Senior Marketing Manager, SoCal Region', 'Current Company': 'Providence', 'Employment Dates': 'Oct 2018 – Present', 'Most Recent Education': 'University of California, Irvine', 'Years Attended': '', 'Degree': 'BA', 'Field of Study': 'Cognitive Sciences (Psychology)', 'Public Profile': 'https://www.linkedin.com/in/shannon-davis-22218837'}, 'Krushita Shah': {'Location': 'Des Plaines, Illinois, United States', 'Current Position': 'Manager of Financial Planning and Analysis', 'Current Company': 'Northwest Community Healthcare', 'Employment Dates': 'Jun 2018 – Present', 'Most Recent Education': 'Keller Graduate School of Management of DeVry University', 'Years Attended': '', 'Degree': 'Master of Accounting and Financial Management', 'Field of Study': '', 'Public Profile': 'https://www.linkedin.com/in/krushita-shah-04047b116'}, 'Brittany Lett': {'Location': 'New York, New York, United States', 'Current Position': 'Vice President of Marketing', 'Current Company': 'AdaptHealth', 'Employment Dates': 'Jul 2018 – Present', 'Most Recent Education': 'University of Southern California - Marshall School of Business', 'Years Attended': '2007 – 2010', 'Degree': 'Bachelor’s Degree', 'Field of Study': 'Business Administration; Concentration: Strategic Management', 'Public Profile': 'https://www.linkedin.com/in/brittanylett'}, 'William C. Bell': {'Location': 'Houston, Texas, United States', 'Current Position': 'Senior Client Services Manager', 'Current Company': 'UnitedHealth Group', 'Employment Dates': 'Feb 2019 – Present', 'Most Recent Education': 'Texas A&M Health Science Center School of Public Health', 'Years Attended': '2013 – 2015', 'Degree': "Master's Degree", 'Field of Study': 'Health/Health Care Administration/Management', 'Public Profile': 'https://www.linkedin.com/in/william-c-bell-mha-98320662'}, 'Robyn Goode': {'Location': 'Towson, Maryland, United States', 'Current Position': 'Corporate HR Manager', 'Current Company': 'Senior Helpers', 'Employment Dates': 'Jan 2018 – Present', 'Most Recent Education': 'Villanova University', 'Years Attended': '', 'Degree': 'Masters', 'Field of Study': 'Human Resources Management', 'Public Profile': 'https://www.linkedin.com/in/robyngoode'}, "Benjamin O'Shea": {'Location': 'Lake Elsinore, California, United States', 'Current Position': 'Senior Manager Business Operations', 'Current Company': 'Community Brands', 'Employment Dates': 'May 2020 – Present', 'Most Recent Education': 'Arizona State University', 'Years Attended': '2018 – 2020', 'Degree': "Bachelor's degree", 'Field of Study': 'History', 'Public Profile': 'https://www.linkedin.com/in/benjaminmoshea'}, 'Taylor Clemmer': {'Location': 'Greater Houston', 'Current Position': 'Chief Operating Officer-National Dental Service Organization Subsidiary', 'Current Company': 'American Dental Partners', 'Employment Dates': 'Sep 2019 – Present', 'Most Recent Education': 'University of Texas at Tyler', 'Years Attended': '', 'Degree': 'Bachelor of Business Administration - BBA', 'Field of Study': 'Business Administration, Management and Operations', 'Public Profile': 'https://www.linkedin.com/in/taylor-clemmer-chpca-fache-b2306a11'}, 'Austin Laughner': {'Location': 'Greater Chicago Area', 'Current Position': 'Senior Project Manager - IT - Business Intelligence', 'Current Company': 'American Medical Association', 'Employment Dates': 'Mar 2017 – Present', 'Most Recent Education': 'Indiana University', 'Years Attended': '2006 – 2009', 'Degree': 'Bachelor of Science', 'Field of Study': 'Finance & Economics', 'Public Profile': 'https://www.linkedin.com/in/austinlaughner'}, 'Harshini Reddy': {'Location': 'New York, New York, United States', 'Current Position': 'Project Manager - Department of Medicine & Hospital Medicine', 'Current Company': 'Northwell Health', 'Employment Dates': 'Sep 2019 – Present', 'Most Recent Education': 'Columbia University Mailman School of Public Health', 'Years Attended': '2014 – 2016', 'Degree': 'Master of Health Administration', 'Field of Study': 'Health/Health Care Administration/Management', 'Public Profile': 'https://www.linkedin.com/in/harshini-reddy-20503091'}, 'Keith Kirby': {'Location': 'Kansas City Metropolitan Area', 'Current Position': 'National Strategic Growth Executive', 'Current Company': 'symplr', 'Employment Dates': 'Jul 2021 – Present', 'Most Recent Education': 'Colorado Technical University', 'Years Attended': '2005 – 2008', 'Degree': 'Bachelor', 'Field of Study': 'Applied Science/ Radiology', 'Public Profile': 'https://www.linkedin.com/in/keith-kirby-4b164b32'}, 'Claudia Soltys': {'Location': 'North Grafton, Massachusetts, United States', 'Current Position': 'Senior HR Manager', 'Current Company': 'Fresenius Medical Care North America', 'Employment Dates': 'Dec 2016 – Present', 'Most Recent Education': 'Assumption College', 'Years Attended': '', 'Degree': 'BA', 'Field of Study': 'Biology/Psychology', 'Public Profile': 'https://www.linkedin.com/in/claudia-soltys-shrm'}, 'Scott Kagan': {'Location': 'Stamford, Connecticut, United States', 'Current Position': 'Regional Manager of Business Development', 'Current Company': 'Labcorp', 'Employment Dates': 'Dec 2018 – Present', 'Most Recent Education': 'Curry College', 'Years Attended': '2001 – 2005', 'Degree': 'Bachelor of Arts', 'Field of Study': 'Major in Psychology, Minor in Communications', 'Public Profile': 'https://www.linkedin.com/in/scott-kagan-8459406'}, 'Jennifer Bruns': {'Location': 'Long Beach, California, United States', 'Current Position': 'Senior HR Business Partner', 'Current Company': 'MemorialCare', 'Employment Dates': 'Oct 2016 – Present', 'Most Recent Education': 'Pepperdine Graziadio Business School', 'Years Attended': '1998 – 2001', 'Degree': 'MBA', 'Field of Study': 'Business Administration', 'Public Profile': 'https://www.linkedin.com/in/jennifer-bruns-mba-sphr-a8029818'}, 'Matthew V. Baker M.S.': {'Location': 'Sandy, Utah, United States', 'Current Position': 'Group Manager--Client Services/Referral Testing', 'Current Company': 'ARUP Laboratories', 'Employment Dates': 'Jul 2019 – Present', 'Most Recent Education': 'Utah State University', 'Years Attended': '2006 – 2008', 'Degree': 'Master of Science (MS)', 'Field of Study': 'Instructional Technology', 'Public Profile': 'https://www.linkedin.com/in/matthew-v-baker-m-s-02591149'}, 'Venus Brady': {'Location': 'Greater Chicago Area', 'Current Position': 'Senior Marketing Communications Specialist', 'Current Company': 'UChicago Medicine', 'Employment Dates': 'Jun 2019 – Present', 'Most Recent Education': 'Elmhurst University', 'Years Attended': '2020 – 2021', 'Degree': 'Graduate Certificate', 'Field of Study': 'Market Research', 'Public Profile': 'https://www.linkedin.com/in/vebra'}, 'Daniel Esquibel': {'Location': 'Greater Chicago Area', 'Current Position': 'Senior Manager', 'Current Company': 'Deloitte', 'Employment Dates': 'Apr 2015 – Present', 'Most Recent Education': 'University of Pennsylvania', 'Years Attended': '1996 – 2000', 'Degree': '', 'Field of Study': '', 'Public Profile': 'https://www.linkedin.com/in/danielesquibel'}, 'Karen Douglas': {'Location': 'Columbus, Ohio Metropolitan Area', 'Current Position': 'Senior Manager, Digital Product & Solutions Marketing', 'Current Company': 'Cardinal Health', 'Employment Dates': 'Jul 2020 – Present', 'Most Recent Education': 'Malone College', 'Years Attended': '1995 – 1999', 'Degree': 'Bachelor of Science', 'Field of Study': 'Education', 'Public Profile': 'https://www.linkedin.com/in/karen-douglas-b68a444'}, 'Mario L.': {'Location': 'Greater Boston', 'Current Position': 'Territory Manager - Advanced Pain Therapies', 'Current Company': 'Medtronic', 'Employment Dates': 'Oct 2015 – Present', 'Most Recent Education': 'San Diego State University-California State University', 'Years Attended': '2005 – 2007', 'Degree': 'BS', 'Field of Study': 'Health Sciences', 'Public Profile': 'https://www.linkedin.com/in/mariolanese'}, 'Heather Williams': {'Location': 'Churubusco, Indiana, United States', 'Current Position': 'Regional Operations Manager', 'Current Company': 'Parkview Health', 'Employment Dates': 'Jan 2019 – Present', 'Most Recent Education': 'Western Governors University', 'Years Attended': '2017 – 2018', 'Degree': 'Masters of Science Management and Leadership', 'Field of Study': '', 'Public Profile': 'https://www.linkedin.com/in/heather-williams-57601195'}, 'Slade Burkeen': {'Location': 'Nashville Metropolitan Area', 'Current Position': 'Manager FP&A', 'Current Company': 'eviCore healthcare', 'Employment Dates': 'Jul 2019 – Present', 'Most Recent Education': 'Texas A&M University', 'Years Attended': '2001 – 2002', 'Degree': 'Master of Science - MS', 'Field of Study': 'Finance', 'Public Profile': 'https://www.linkedin.com/in/slade-burkeen-8a605213b'}, 'Stephanie Mears': {'Location': 'Charleston, South Carolina, United States', 'Current Position': 'Area Vice President', 'Current Company': 'Kindred Hospice', 'Employment Dates': 'Nov 2019 – May 2021', 'Most Recent Education': 'School Of Music United States Army', 'Years Attended': '1978 – 1982', 'Degree': 'Music Performance and Education', 'Field of Study': 'Music', 'Public Profile': 'https://www.linkedin.com/in/stephanie-mears-b6371415'}, 'Kenya Howard': {'Location': 'Concord, California, United States', 'Current Position': 'Div HR Director, BP', 'Current Company': 'Falck', 'Employment Dates': 'Sep 2019 – Present', 'Most Recent Education': 'Holy Names University', 'Years Attended': '2010 – 2012', 'Degree': 'MBA', 'Field of Study': 'Finance', 'Public Profile': 'https://www.linkedin.com/in/kenya-howard-mba-68a46436'}, 'Katherine Lutz': {'Location': 'Boston, Massachusetts, United States', 'Current Position': 'Group Marketing Manager', 'Current Company': "Boston Children's Hospital", 'Employment Dates': 'Oct 2018 – Present', 'Most Recent Education': 'Boston University', 'Years Attended': '', 'Degree': 'MS', 'Field of Study': 'Science Journalism', 'Public Profile': 'https://www.linkedin.com/in/katherine-lutz'}, 'Thurston Stephens': {'Location': 'Nashville, Tennessee, United States', 'Current Position': 'Regional Payer Contracting Manager', 'Current Company': 'Sound Physicians', 'Employment Dates': 'Aug 2019 – Present', 'Most Recent Education': 'Tusculum College', 'Years Attended': '2006 – 2008', 'Degree': 'Bachelor of Science (BS)', 'Field of Study': 'Business Administration, Management and Operations', 'Public Profile': 'https://www.linkedin.com/in/thurston-stephens-99933664'}, 'Nichelle Gibbs': {'Location': 'Baltimore, Maryland, United States', 'Current Position': 'Senior Human Resources Business Partner', 'Current Company': 'GBMC HealthCare', 'Employment Dates': 'Sep 2018 – Present', 'Most Recent Education': 'University of Maryland University College', 'Years Attended': '2011 – 2014', 'Degree': "Master's degree", 'Field of Study': 'Human Resources Management and Services', 'Public Profile': 'https://www.linkedin.com/in/nichelle-gibbs-phr-0b5bb360'}, 'Richard Winters': {'Location': 'Winter Garden, Florida, United States', 'Current Position': 'Vice President of Human Resources', 'Current Company': 'New Season', 'Employment Dates': 'Mar 2020 – Present', 'Most Recent Education': 'Florida International University - College of Business', 'Years Attended': '2015 – 2018', 'Degree': 'Master of Business Administration (M.B.A.)', 'Field of Study': 'Business/Corporate Communications', 'Public Profile': 'https://www.linkedin.com/in/richard-winters-mba-sphr-52110a9'}, 'Kacie Moody': {'Location': 'Greater Pittsburgh Region', 'Current Position': 'Client Services Manager', 'Current Company': 'Cotiviti', 'Employment Dates': 'Feb 2020 – Present', 'Most Recent Education': 'Saint Vincent College', 'Years Attended': '2005 – 2009', 'Degree': 'Bachelor of Business Administration (B.B.A.)', 'Field of Study': 'Business Administration and Management, General', 'Public Profile': 'https://www.linkedin.com/in/kacie-moody-59924754'}, 'Timothy Chadwick': {'Location': 'Sparks, Nevada, United States', 'Current Position': 'Store Manager', 'Current Company': 'CVS Health', 'Employment Dates': 'Apr 2018 – Present', 'Most Recent Education': 'The University of New Mexico', 'Years Attended': '2014 – 2018', 'Degree': '', 'Field of Study': '', 'Public Profile': 'https://www.linkedin.com/in/timothy-chadwick-390a83140'}, 'Britta Nally': {'Location': 'Denver, Colorado, United States', 'Current Position': 'Project Manager - Disaster Health Response System', 'Current Company': 'Denver Health', 'Employment Dates': 'Apr 2021 – Present', 'Most Recent Education': 'Northwestern University - The Feinberg School of Medicine', 'Years Attended': '2017 – 2019', 'Degree': 'Master of Healthcare Quality and Patient Safety', 'Field of Study': '', 'Public Profile': 'https://www.linkedin.com/in/britta-nally'}, 'Rob Adhikari MBA': {'Location': 'Los Angeles Metropolitan Area', 'Current Position': 'Vice President - Partner Development', 'Current Company': 'Evolent Health', 'Employment Dates': 'Feb 2019 – Present', 'Most Recent Education': 'Rutgers University', 'Years Attended': '1991 – 1995', 'Degree': 'Bachelor of Arts (BA)', 'Field of Study': 'Molecular Biology & BioChemistry', 'Public Profile': 'https://www.linkedin.com/in/robadhikari'}, 'Adrian Castro': {'Location': 'Glendale, Arizona, United States', 'Current Position': 'Area Operations Manager', 'Current Company': 'NextCare Urgent Care', 'Employment Dates': '2013 – Present', 'Most Recent Education': 'University of Phoenix', 'Years Attended': '2014 – 2017', 'Degree': 'Bachelor’s degree', 'Field of Study': 'Business Administration and Management, GeneralBusiness administration', 'Public Profile': 'https://www.linkedin.com/in/adrian-castro-3820051a3'}}
    
    dict_less_email = apollo_href(dict_less_apollo)
    # print(dict_less_email)
    
    #dict_less_email = {'Kyle Allen': {'Location': 'Dallas-Fort Worth Metroplex', 'Current Position': 'Regional Business Development Manager', 'Current Company': 'Sound Physicians', 'Employment Dates': 'Oct 2014 – Present', 'Most Recent Education': '', 'Years Attended': '', 'Degree': '', 'Field of Study': '', 'Public Profile': 'https://www.linkedin.com/in/kyle-allen-405aaa40', 'Apollo Link': 'https://app.apollo.io/#/contacts/6106f08d323c7a012e839300'}, 'Helen Wainwright': {'Location': 'Sacramento, California, United States', 'Current Position': 'Regional Business Development Manager', 'Current Company': 'Sound Physicians', 'Employment Dates': 'Oct 2014 – Present', 'Most Recent Education': '', 'Years Attended': '', 'Degree': '', 'Field of Study': '', 'Public Profile': 'https://www.linkedin.com/in/helen-wainwright-shrm-scp-9428a66', 'Apollo Link': 'https://app.apollo.io/#/contacts/6106f08d323c7a012e839300'}, 'J.D. Pohutsky': {'Location': 'Fort Lauderdale, Florida, United States', 'Current Position': 'Territory Manager - Advanced Endoscopic Technologies', 'Current Company': 'CONMED Corporation', 'Employment Dates': 'Mar 2020 – Present', 'Most Recent Education': 'University of Mississippi', 'Years Attended': '2010 – 2016', 'Degree': 'Bachelor of Science in Criminal Justice', 'Field of Study': 'Emphasis - Homeland Security', 'Public Profile': 'https://www.linkedin.com/in/j-d-pohutsky-a7a29788', 'Apollo Link': 'https://app.apollo.io/#/contacts/6106f08d323c7a012e839300'}, 'Kristine Phisayavong': {'Location': 'Orange County, California, United States', 'Current Position': 'Territory Sales Manager', 'Current Company': 'Benco Dental', 'Employment Dates': 'Apr 2019 – Jun 2021', 'Most Recent Education': 'Orange Coast College', 'Years Attended': '1987 – 1992', 'Degree': 'Associate of Arts - AA', 'Field of Study': 'Business and Personal/Financial Services Marketing Operations', 'Public Profile': 'https://www.linkedin.com/in/kristine-phisayavong-93812060', 'Apollo Link': 'https://app.apollo.io/#/contacts/610b251fe797b900a47aaa8e'}, 'Mike Snoy': {'Location': 'Ogden, Utah, United States', 'Current Position': 'Market Sales Manager', 'Current Company': 'Center for Diagnostic Imaging (CDI)', 'Employment Dates': 'Oct 2020 – Present', 'Most Recent Education': 'Weber State University', 'Years Attended': '2006 – 2010', 'Degree': 'Technical Sales (B.S.)', 'Field of Study': 'Sales, Distribution, and Marketing Operations, General', 'Public Profile': 'https://www.linkedin.com/in/mikesnoy', 'Apollo Link': 'https://app.apollo.io/#/contacts/610b245f8b18cf00f69ff51e'}, 'Vikki Carter': {'Location': 'Nashville, Tennessee, United States', 'Current Position': 'Regional Business Development Manager', 'Current Company': 'Sound Physicians', 'Employment Dates': 'May 2020 – Present', 'Most Recent Education': 'Western Kentucky University', 'Years Attended': '', 'Degree': 'BA', 'Field of Study': 'Advertising', 'Public Profile': 'https://www.linkedin.com/in/vikkiecarter', 'Apollo Link': 'https://app.apollo.io/#/contacts/6108b518f7b28400dbc1a3be'}, 'Julie Angelos': {'Location': 'Santa Barbara County, California, United States', 'Current Position': 'Professional Sales Representative', 'Current Company': 'Takeda', 'Employment Dates': 'Sep 2018 – Present', 'Most Recent Education': 'Westmont College', 'Years Attended': '2000 – 2003', 'Degree': 'BA', 'Field of Study': 'Social Science, Business', 'Public Profile': 'https://www.linkedin.com/in/julie-angelos-7598858', 'Apollo Link': 'https://app.apollo.io/#/people/5e655f856a43380001084b4a'}, 'Joe Grilli': {'Location': 'Bloomfield, New Jersey, United States', 'Current Position': 'Client Services Manager', 'Current Company': '365 Health Services, LLC', 'Employment Dates': 'Sep 2020 – Present', 'Most Recent Education': 'Rowan University', 'Years Attended': '2016 – 2020', 'Degree': '3.5 years', 'Field of Study': 'Marketing', 'Public Profile': 'https://www.linkedin.com/in/joe-grilli', 'Apollo Link': 'https://app.apollo.io/#/contacts/610b244adb786f00f67e0aa5'}, 'Hally Kocur': {'Location': 'Estero, Florida, United States', 'Current Position': 'Digital Marketing Manager', 'Current Company': 'GenesisCare', 'Employment Dates': 'Sep 2020 – Present', 'Most Recent Education': 'Florida Gulf Coast University', 'Years Attended': '2012 – 2013', 'Degree': 'Bachelor of Arts (B.A.)', 'Field of Study': 'Communication, General', 'Public Profile': 'https://www.linkedin.com/in/hally-kocur-a9b20813a', 'Apollo Link': 'https://app.apollo.io/#/contacts/610b69b0c0f0cf00dad3b8e7'}, 'Melissa Mushlin': {'Location': 'Greater St. Louis', 'Current Position': 'Senior Business Development Manager', 'Current Company': 'Cross Country Healthcare', 'Employment Dates': '2014 – Present', 'Most Recent Education': 'Way of Life Seminary', 'Years Attended': '', 'Degree': "Bachelor's Degree", 'Field of Study': 'Christian Education', 'Public Profile': 'https://www.linkedin.com/in/melissamushlin', 'Apollo Link': 'https://app.apollo.io/#/contacts/6106f102323c7a00a49086e4'}, 'Michael Sweetser': {'Location': 'Greater Tampa Bay Area', 'Current Position': 'Manager of Broker Sales', 'Current Company': 'Teladoc Health', 'Employment Dates': 'Feb 2020 – Present', 'Most Recent Education': 'Wake Forest University', 'Years Attended': '2009 – 2013', 'Degree': 'Bachelor of Arts (B.A.)', 'Field of Study': 'History & Political Science', 'Public Profile': 'https://www.linkedin.com/in/michael-sweetser-a737bb30', 'Apollo Link': 'https://app.apollo.io/#/contacts/6106f0afc205670112638e64'}, 'Julie Keiper': {'Location': 'Waynesville, North Carolina, United States', 'Current Position': 'Provider Account Executive II /Region 1 Lead/Tribal Liaison', 'Current Company': 'AmeriHealth Caritas', 'Employment Dates': 'Jun 2019 – Present', 'Most Recent Education': 'University of Minnesota-Duluth', 'Years Attended': '', 'Degree': 'Bachelor of Arts', 'Field of Study': 'Business / Psychology', 'Public Profile': 'https://www.linkedin.com/in/jakeiper', 'Apollo Link': 'https://app.apollo.io/#/contacts/610b245ae797b900a47aa5dc'}, 'Brendan Dee': {'Location': 'North Reading, Massachusetts, United States', 'Current Position': 'Territory Sales Manager', 'Current Company': 'Philips', 'Employment Dates': 'Nov 2019 – Present', 'Most Recent Education': 'University of Massachusetts, Amherst', 'Years Attended': '', 'Degree': 'Bachelor of Arts (B.A.)', 'Field of Study': 'Communications', 'Public Profile': 'https://www.linkedin.com/in/brendan-dee-13110a70', 'Apollo Link': 'https://app.apollo.io/#/contacts/610b5eebc78fb200dc1a5ef1'}, 'Kara Stead': {'Location': 'Woodbridge, Virginia, United States', 'Current Position': 'Human Resources Business Partner', 'Current Company': 'Mary Washington Healthcare', 'Employment Dates': 'Nov 2019 – Present', 'Most Recent Education': 'Goucher College', 'Years Attended': '', 'Degree': "Bachelor's degree", 'Field of Study': 'English (Writing)', 'Public Profile': 'https://www.linkedin.com/in/kara-stead-shrm-cp-37458815', 'Apollo Link': 'https://app.apollo.io/#/contacts/6108b53932973a00a4849fb6'}, 'Bradley Smith': {'Location': 'Nashville Metropolitan Area', 'Current Position': 'Regional Sales Manager', 'Current Company': 'Fresenius Medical Care North America', 'Employment Dates': 'Aug 2020 – Present', 'Most Recent Education': 'Indiana University Bloomington', 'Years Attended': '2000 – 2003', 'Degree': 'Bachelor of Arts', 'Field of Study': 'History and Mathematics', 'Public Profile': 'https://www.linkedin.com/in/bradley-smith-88339121', 'Apollo Link': 'https://app.apollo.io/#/people/5ae3a6e2a6da98d36d7a28a7'}, 'Colette Colburn': {'Location': 'Seattle, Washington, United States', 'Current Position': 'Program Manager, Strategic Accounts', 'Current Company': 'AMN Healthcare', 'Employment Dates': 'Feb 2019 – Present', 'Most Recent Education': 'Seattle University', 'Years Attended': '1986 – 1991', 'Degree': 'Bachelor of Arts (B.A.)', 'Field of Study': 'History and French', 'Public Profile': 'https://www.linkedin.com/in/colettecolburn', 'Apollo Link': None}, 'James Taylor': {'Location': 'Boca Raton, Florida, United States', 'Current Position': 'Regional Sales Manager, Strategic Accounts - Orthopedics', 'Current Company': 'Modernizing Medicine', 'Employment Dates': 'Jan 2021 – Present', 'Most Recent Education': 'Boston College', 'Years Attended': '2013 – 2017', 'Degree': 'Bachelor of Arts (B.A.)', 'Field of Study': 'Economics', 'Public Profile': 'https://www.linkedin.com/in/james-taylor-514478112', 'Apollo Link': 'https://app.apollo.io/#/contacts/610c0e6c4e520a00a430cf0f'}, 'Erika Swift': {'Location': 'Orange County, California, United States', 'Current Position': 'Senior Clinical Manager', 'Current Company': 'naviHealth', 'Employment Dates': 'Feb 2014 – Present', 'Most Recent Education': 'Northwestern University', 'Years Attended': '', 'Degree': 'Master of Science - MS', 'Field of Study': 'Health Analytics', 'Public Profile': 'https://www.linkedin.com/in/erika-swift-75964582', 'Apollo Link': 'https://app.apollo.io/#/contacts/610b24e7974fcf00f6b88c6b'}, 'James Heinlen': {'Location': 'Phoenix, Arizona, United States', 'Current Position': 'Call Center Manager', 'Current Company': 'Dignity Health', 'Employment Dates': 'Mar 2018 – Present', 'Most Recent Education': 'Ashford University', 'Years Attended': '2018 – 2020', 'Degree': 'Master of Business Administration - MBA', 'Field of Study': 'Organizational Leadership', 'Public Profile': 'https://www.linkedin.com/in/james-heinlen-mba-23556220', 'Apollo Link': 'https://app.apollo.io/#/contacts/6106f11be014220112a8c81a'}, 'Shannon Davis': {'Location': 'Los Angeles Metropolitan Area', 'Current Position': 'Senior Marketing Manager, SoCal Region', 'Current Company': 'Providence', 'Employment Dates': 'Oct 2018 – Present', 'Most Recent Education': 'University of California, Irvine', 'Years Attended': '', 'Degree': 'BA', 'Field of Study': 'Cognitive Sciences (Psychology)', 'Public Profile': 'https://www.linkedin.com/in/shannon-davis-22218837', 'Apollo Link': 'https://app.apollo.io/#/contacts/6106f13779aa3000a43e113c'}, 'Krushita Shah': {'Location': 'Des Plaines, Illinois, United States', 'Current Position': 'Manager of Financial Planning and Analysis', 'Current Company': 'Northwest Community Healthcare', 'Employment Dates': 'Jun 2018 – Present', 'Most Recent Education': 'Keller Graduate School of Management of DeVry University', 'Years Attended': '', 'Degree': 'Master of Accounting and Financial Management', 'Field of Study': '', 'Public Profile': 'https://www.linkedin.com/in/krushita-shah-04047b116', 'Apollo Link': 'https://app.apollo.io/#/contacts/6106f0e34cca4100a420322b'}, 'Brittany Lett': {'Location': 'New York, New York, United States', 'Current Position': 'Vice President of Marketing', 'Current Company': 'AdaptHealth', 'Employment Dates': 'Jul 2018 – Present', 'Most Recent Education': 'University of Southern California - Marshall School of Business', 'Years Attended': '2007 – 2010', 'Degree': 'Bachelor’s Degree', 'Field of Study': 'Business Administration; Concentration: Strategic Management', 'Public Profile': 'https://www.linkedin.com/in/brittanylett', 'Apollo Link': 'https://app.apollo.io/#/contacts/6108b57ae7c55400da871c9d'}, 'William C. Bell': {'Location': 'Houston, Texas, United States', 'Current Position': 'Senior Client Services Manager', 'Current Company': 'UnitedHealth Group', 'Employment Dates': 'Feb 2019 – Present', 'Most Recent Education': 'Texas A&M Health Science Center School of Public Health', 'Years Attended': '2013 – 2015', 'Degree': "Master's Degree", 'Field of Study': 'Health/Health Care Administration/Management', 'Public Profile': 'https://www.linkedin.com/in/william-c-bell-mha-98320662', 'Apollo Link': 'https://app.apollo.io/#/people/60ea050f0e5e700001fab392'}, 'Robyn Goode': {'Location': 'Towson, Maryland, United States', 'Current Position': 'Corporate HR Manager', 'Current Company': 'Senior Helpers', 'Employment Dates': 'Jan 2018 – Present', 'Most Recent Education': 'Villanova University', 'Years Attended': '', 'Degree': 'Masters', 'Field of Study': 'Human Resources Management', 'Public Profile': 'https://www.linkedin.com/in/robyngoode', 'Apollo Link': 'https://app.apollo.io/#/contacts/6108b5277f6f7900f6e5ec13'}, "Benjamin O'Shea": {'Location': 'Lake Elsinore, California, United States', 'Current Position': 'Senior Manager Business Operations', 'Current Company': 'Community Brands', 'Employment Dates': 'May 2020 – Present', 'Most Recent Education': 'Arizona State University', 'Years Attended': '2018 – 2020', 'Degree': "Bachelor's degree", 'Field of Study': 'History', 'Public Profile': 'https://www.linkedin.com/in/benjaminmoshea', 'Apollo Link': 'https://app.apollo.io/#/contacts/610c0eb7fbec1200a4403da8'}, 'Taylor Clemmer': {'Location': 'Greater Houston', 'Current Position': 'Chief Operating Officer-National Dental Service Organization Subsidiary', 'Current Company': 'American Dental Partners', 'Employment Dates': 'Sep 2019 – Present', 'Most Recent Education': 'University of Texas at Tyler', 'Years Attended': '', 'Degree': 'Bachelor of Business Administration - BBA', 'Field of Study': 'Business Administration, Management and Operations', 'Public Profile': 'https://www.linkedin.com/in/taylor-clemmer-chpca-fache-b2306a11', 'Apollo Link': 'https://app.apollo.io/#/contacts/6108b5cb3adcde00a532dd48'}, 'Austin Laughner': {'Location': 'Greater Chicago Area', 'Current Position': 'Senior Project Manager - IT - Business Intelligence', 'Current Company': 'American Medical Association', 'Employment Dates': 'Mar 2017 – Present', 'Most Recent Education': 'Indiana University', 'Years Attended': '2006 – 2009', 'Degree': 'Bachelor of Science', 'Field of Study': 'Finance & Economics', 'Public Profile': 'https://www.linkedin.com/in/austinlaughner', 'Apollo Link': 'https://app.apollo.io/#/contacts/6108b5cb3adcde00a532dd48'}, 'Harshini Reddy': {'Location': 'New York, New York, United States', 'Current Position': 'Project Manager - Department of Medicine & Hospital Medicine', 'Current Company': 'Northwell Health', 'Employment Dates': 'Sep 2019 – Present', 'Most Recent Education': 'Columbia University Mailman School of Public Health', 'Years Attended': '2014 – 2016', 'Degree': 'Master of Health Administration', 'Field of Study': 'Health/Health Care Administration/Management', 'Public Profile': 'https://www.linkedin.com/in/harshini-reddy-20503091', 'Apollo Link': 'https://app.apollo.io/#/contacts/610c184e511f9f00a49e16dd'}, 'Keith Kirby': {'Location': 'Kansas City Metropolitan Area', 'Current Position': 'National Strategic Growth Executive', 'Current Company': 'symplr', 'Employment Dates': 'Jul 2021 – Present', 'Most Recent Education': 'Colorado Technical University', 'Years Attended': '2005 – 2008', 'Degree': 'Bachelor', 'Field of Study': 'Applied Science/ Radiology', 'Public Profile': 'https://www.linkedin.com/in/keith-kirby-4b164b32', 'Apollo Link': 'https://app.apollo.io/#/contacts/6108b55231073f00a41cb367'}, 'Claudia Soltys': {'Location': 'North Grafton, Massachusetts, United States', 'Current Position': 'Senior HR Manager', 'Current Company': 'Fresenius Medical Care North America', 'Employment Dates': 'Dec 2016 – Present', 'Most Recent Education': 'Assumption College', 'Years Attended': '', 'Degree': 'BA', 'Field of Study': 'Biology/Psychology', 'Public Profile': 'https://www.linkedin.com/in/claudia-soltys-shrm', 'Apollo Link': 'https://app.apollo.io/#/people/61070c77d99d510001da9034'}, 'Scott Kagan': {'Location': 'Stamford, Connecticut, United States', 'Current Position': 'Regional Manager of Business Development', 'Current Company': 'Labcorp', 'Employment Dates': 'Dec 2018 – Present', 'Most Recent Education': 'Curry College', 'Years Attended': '2001 – 2005', 'Degree': 'Bachelor of Arts', 'Field of Study': 'Major in Psychology, Minor in Communications', 'Public Profile': 'https://www.linkedin.com/in/scott-kagan-8459406', 'Apollo Link': 'https://app.apollo.io/#/contacts/6108b594e7c55400da871d22'}, 'Jennifer Bruns': {'Location': 'Long Beach, California, United States', 'Current Position': 'Senior HR Business Partner', 'Current Company': 'MemorialCare', 'Employment Dates': 'Oct 2016 – Present', 'Most Recent Education': 'Pepperdine Graziadio Business School', 'Years Attended': '1998 – 2001', 'Degree': 'MBA', 'Field of Study': 'Business Administration', 'Public Profile': 'https://www.linkedin.com/in/jennifer-bruns-mba-sphr-a8029818', 'Apollo Link': 'https://app.apollo.io/#/contacts/610b2581db786f00a47e834f'}, 'Matthew V. Baker M.S.': {'Location': 'Sandy, Utah, United States', 'Current Position': 'Group Manager--Client Services/Referral Testing', 'Current Company': 'ARUP Laboratories', 'Employment Dates': 'Jul 2019 – Present', 'Most Recent Education': 'Utah State University', 'Years Attended': '2006 – 2008', 'Degree': 'Master of Science (MS)', 'Field of Study': 'Instructional Technology', 'Public Profile': 'https://www.linkedin.com/in/matthew-v-baker-m-s-02591149', 'Apollo Link': 'https://app.apollo.io/#/people/5ef6ce1ed9292f0001746766'}, 'Venus Brady': {'Location': 'Greater Chicago Area', 'Current Position': 'Senior Marketing Communications Specialist', 'Current Company': 'UChicago Medicine', 'Employment Dates': 'Jun 2019 – Present', 'Most Recent Education': 'Elmhurst University', 'Years Attended': '2020 – 2021', 'Degree': 'Graduate Certificate', 'Field of Study': 'Market Research', 'Public Profile': 'https://www.linkedin.com/in/vebra', 'Apollo Link': 'https://app.apollo.io/#/contacts/6106f0a64cca4100a42030b4'}, 'Daniel Esquibel': {'Location': 'Greater Chicago Area', 'Current Position': 'Senior Manager', 'Current Company': 'Deloitte', 'Employment Dates': 'Apr 2015 – Present', 'Most Recent Education': 'University of Pennsylvania', 'Years Attended': '1996 – 2000', 'Degree': '', 'Field of Study': '', 'Public Profile': 'https://www.linkedin.com/in/danielesquibel', 'Apollo Link': 'https://app.apollo.io/#/contacts/6106f0f2323c7a00da8c02d4'}, 'Karen Douglas': {'Location': 'Columbus, Ohio Metropolitan Area', 'Current Position': 'Senior Manager, Digital Product & Solutions Marketing', 'Current Company': 'Cardinal Health', 'Employment Dates': 'Jul 2020 – Present', 'Most Recent Education': 'Malone College', 'Years Attended': '1995 – 1999', 'Degree': 'Bachelor of Science', 'Field of Study': 'Education', 'Public Profile': 'https://www.linkedin.com/in/karen-douglas-b68a444', 'Apollo Link': 'https://app.apollo.io/#/people/6046401dd24e290001175155'}, 'Mario L.': {'Location': 'Greater Boston', 'Current Position': 'Territory Manager - Advanced Pain Therapies', 'Current Company': 'Medtronic', 'Employment Dates': 'Oct 2015 – Present', 'Most Recent Education': 'San Diego State University-California State University', 'Years Attended': '2005 – 2007', 'Degree': 'BS', 'Field of Study': 'Health Sciences', 'Public Profile': 'https://www.linkedin.com/in/mariolanese', 'Apollo Link': 'https://app.apollo.io/#/people/54a412f67468693b8c79332a'}, 'Heather Williams': {'Location': 'Churubusco, Indiana, United States', 'Current Position': 'Regional Operations Manager', 'Current Company': 'Parkview Health', 'Employment Dates': 'Jan 2019 – Present', 'Most Recent Education': 'Western Governors University', 'Years Attended': '2017 – 2018', 'Degree': 'Masters of Science Management and Leadership', 'Field of Study': '', 'Public Profile': 'https://www.linkedin.com/in/heather-williams-57601195', 'Apollo Link': 'https://app.apollo.io/#/contacts/610b5f81c78fb200f81a27c1'}, 'Slade Burkeen': {'Location': 'Nashville Metropolitan Area', 'Current Position': 'Manager FP&A', 'Current Company': 'eviCore healthcare', 'Employment Dates': 'Jul 2019 – Present', 'Most Recent Education': 'Texas A&M University', 'Years Attended': '2001 – 2002', 'Degree': 'Master of Science - MS', 'Field of Study': 'Finance', 'Public Profile': 'https://www.linkedin.com/in/slade-burkeen-8a605213b', 'Apollo Link': 'https://app.apollo.io/#/contacts/610b244fe797b900f87a4f99'}, 'Stephanie Mears': {'Location': 'Charleston, South Carolina, United States', 'Current Position': 'Area Vice President', 'Current Company': 'Kindred Hospice', 'Employment Dates': 'Nov 2019 – May 2021', 'Most Recent Education': 'School Of Music United States Army', 'Years Attended': '1978 – 1982', 'Degree': 'Music Performance and Education', 'Field of Study': 'Music', 'Public Profile': 'https://www.linkedin.com/in/stephanie-mears-b6371415', 'Apollo Link': 'https://app.apollo.io/#/contacts/610b2501577f1200da0a0925'}, 'Kenya Howard': {'Location': 'Concord, California, United States', 'Current Position': 'Div HR Director, BP', 'Current Company': 'Falck', 'Employment Dates': 'Sep 2019 – Present', 'Most Recent Education': 'Holy Names University', 'Years Attended': '2010 – 2012', 'Degree': 'MBA', 'Field of Study': 'Finance', 'Public Profile': 'https://www.linkedin.com/in/kenya-howard-mba-68a46436', 'Apollo Link': 'https://app.apollo.io/#/contacts/610b5f3854adad00f69152a9'}, 'Katherine Lutz': {'Location': 'Boston, Massachusetts, United States', 'Current Position': 'Group Marketing Manager', 'Current Company': "Boston Children's Hospital", 'Employment Dates': 'Oct 2018 – Present', 'Most Recent Education': 'Boston University', 'Years Attended': '', 'Degree': 'MS', 'Field of Study': 'Science Journalism', 'Public Profile': 'https://www.linkedin.com/in/katherine-lutz', 'Apollo Link': 'https://app.apollo.io/#/people/5ff1336d3f31ca00015fb842'}, 'Thurston Stephens': {'Location': 'Nashville, Tennessee, United States', 'Current Position': 'Regional Payer Contracting Manager', 'Current Company': 'Sound Physicians', 'Employment Dates': 'Aug 2019 – Present', 'Most Recent Education': 'Tusculum College', 'Years Attended': '2006 – 2008', 'Degree': 'Bachelor of Science (BS)', 'Field of Study': 'Business Administration, Management and Operations', 'Public Profile': 'https://www.linkedin.com/in/thurston-stephens-99933664', 'Apollo Link': 'https://app.apollo.io/#/contacts/610b5fa4c0f0cf00f6d34d08'}, 'Nichelle Gibbs': {'Location': 'Baltimore, Maryland, United States', 'Current Position': 'Senior Human Resources Business Partner', 'Current Company': 'GBMC HealthCare', 'Employment Dates': 'Sep 2018 – Present', 'Most Recent Education': 'University of Maryland University College', 'Years Attended': '2011 – 2014', 'Degree': "Master's degree", 'Field of Study': 'Human Resources Management and Services', 'Public Profile': 'https://www.linkedin.com/in/nichelle-gibbs-phr-0b5bb360', 'Apollo Link': 'https://app.apollo.io/#/contacts/610b5fa4c0f0cf00f6d34d08'}, 'Richard Winters': {'Location': 'Winter Garden, Florida, United States', 'Current Position': 'Vice President of Human Resources', 'Current Company': 'New Season', 'Employment Dates': 'Mar 2020 – Present', 'Most Recent Education': 'Florida International University - College of Business', 'Years Attended': '2015 – 2018', 'Degree': 'Master of Business Administration (M.B.A.)', 'Field of Study': 'Business/Corporate Communications', 'Public Profile': 'https://www.linkedin.com/in/richard-winters-mba-sphr-52110a9', 'Apollo Link': 'https://app.apollo.io/#/contacts/6108b6d7f7b28400dbc1acac'}, 'Kacie Moody': {'Location': 'Greater Pittsburgh Region', 'Current Position': 'Client Services Manager', 'Current Company': 'Cotiviti', 'Employment Dates': 'Feb 2020 – Present', 'Most Recent Education': 'Saint Vincent College', 'Years Attended': '2005 – 2009', 'Degree': 'Bachelor of Business Administration (B.B.A.)', 'Field of Study': 'Business Administration and Management, General', 'Public Profile': 'https://www.linkedin.com/in/kacie-moody-59924754', 'Apollo Link': None}, 'Timothy Chadwick': {'Location': 'Sparks, Nevada, United States', 'Current Position': 'Store Manager', 'Current Company': 'CVS Health', 'Employment Dates': 'Apr 2018 – Present', 'Most Recent Education': 'The University of New Mexico', 'Years Attended': '2014 – 2018', 'Degree': '', 'Field of Study': '', 'Public Profile': 'https://www.linkedin.com/in/timothy-chadwick-390a83140', 'Apollo Link': 'https://app.apollo.io/#/contacts/610c0f6c82d3c100a48f7cd7'}, 'Britta Nally': {'Location': 'Denver, Colorado, United States', 'Current Position': 'Project Manager - Disaster Health Response System', 'Current Company': 'Denver Health', 'Employment Dates': 'Apr 2021 – Present', 'Most Recent Education': 'Northwestern University - The Feinberg School of Medicine', 'Years Attended': '2017 – 2019', 'Degree': 'Master of Healthcare Quality and Patient Safety', 'Field of Study': '', 'Public Profile': 'https://www.linkedin.com/in/britta-nally', 'Apollo Link': None}, 'Rob Adhikari MBA': {'Location': 'Los Angeles Metropolitan Area', 'Current Position': 'Vice President - Partner Development', 'Current Company': 'Evolent Health', 'Employment Dates': 'Feb 2019 – Present', 'Most Recent Education': 'Rutgers University', 'Years Attended': '1991 – 1995', 'Degree': 'Bachelor of Arts (BA)', 'Field of Study': 'Molecular Biology & BioChemistry', 'Public Profile': 'https://www.linkedin.com/in/robadhikari', 'Apollo Link': 'https://app.apollo.io/#/people/5aa97389a6da987e585da870'}, 'Adrian Castro': {'Location': 'Glendale, Arizona, United States', 'Current Position': 'Area Operations Manager', 'Current Company': 'NextCare Urgent Care', 'Employment Dates': '2013 – Present', 'Most Recent Education': 'University of Phoenix', 'Years Attended': '2014 – 2017', 'Degree': 'Bachelor’s degree', 'Field of Study': 'Business Administration and Management, GeneralBusiness administration', 'Public Profile': 'https://www.linkedin.com/in/adrian-castro-3820051a3', 'Apollo Link': 'https://app.apollo.io/#/people/5c6c9acef6512519ad8682d8'}}
    
    for l in dict_less_email:
        data = dict_less_email[l]
        link = data['Apollo Link']
        if link:
            driver.get(link)                
            if check_exists_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/form/div[1]/div') == True:
                print('gotta log in')
                google_login = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#provider-mounter > div > div.zp_2Pnik > div.zp_2YB95 > div > div.zp_1QN2s > div > div.zp_p7Ra4.zp_2ZLGm > div > form > div:nth-child(1) > div")))
                google_login.click()
                try:
                    memail = driver.find_element_by_id("identifierId")
                    memail.send_keys('wsheehan.spiritmco@gmail.com')
                    next_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#identifierNext > div > button > span")))
                    next_button.click()
                except NoSuchElementException:
                    print('auto login')
                
                driver.get(link)
                time.sleep(2)                
            
            if check_exists_by_css("button.zp-button:nth-child(2) > div:nth-child(2)") == True:
                access = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.zp-button:nth-child(2) > div:nth-child(2)")))
                try:
                    access.click()
                except StaleElementReferenceException:
                    time.sleep(4)
                    try:
                        access.click()
                    except StaleElementReferenceException:
                        continue
                time.sleep(2)
                try:
                    email = driver.find_element_by_css_selector('.zp_3v1d1').text
                    print(email)
                except ElementNotInteractableException:
                    print('no email on page')
                    email = ''
            else:    
                try:
                    email = driver.find_element_by_css_selector('.zp_3v1d1').text
                    print(email)
                except ElementNotInteractableException:
                    print('no email on page')
                    email = ''
        else:
            email = ''
        
        if 'No ema' in email:
            email = ''
            
        
        data['Email'] = email   
        out_dict[l] = data
        
    print(out_dict)
    
    save_to_file(out_dict, output_name)
    
    
    
    
    
root = tk.Tk()

canvas = tk.Canvas(root, height=700, width=800)
canvas.pack()

frame = tk.Frame(root, bg='gray')
frame.place(relwidth=1, relheight=1)

label_url = tk.Label(frame, text='URL')
label_url.grid(row=1, column=0)

entry_url = tk.Entry(frame)
entry_url.grid(row=1, column=1)

label_pages = tk.Label(frame, text='# Pages')
label_pages.grid(row=2, column=0)

entry_pages = tk.Entry(frame)
entry_pages.grid(row=2, column=1)

label_outputname = tk.Label(frame, text = 'Output name (eg. "NPO5kleaders")')
label_outputname.grid(row=3, column=0)

entry_outputname = tk.Entry(frame)
entry_outputname.grid(row=3, column=1)

button = tk.Button(frame, text = 'Go!', command= lambda: get_email(entry_url.get(), entry_pages.get(), entry_outputname.get()))
button.grid(row=3, column=4)



root.mainloop()



